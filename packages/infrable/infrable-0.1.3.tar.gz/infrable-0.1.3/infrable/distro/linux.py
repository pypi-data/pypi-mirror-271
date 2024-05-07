from dataclasses import dataclass, field
from shlex import quote as q
from typing import Optional

from infrable import errors
from infrable.host import Host


@dataclass(unsafe_hash=True, order=True, eq=True)
class LinuxLatestHost(Host):
    """A latest version of generic Linux host."""

    authorized_keys: str = ""
    users: dict[str, dict[str, str]] = field(default_factory=dict)

    def setup(self, as_root: bool = False):
        self.ensure_admin(as_root=as_root)
        self.disable_root_login()
        self.ensure_hostname()
        self.ensure_users()

    def ensure_hostname(self, fqdn: str | None = None):
        fqdn = fqdn or self.fqdn
        if not fqdn:
            raise errors.FQDNMustNotBeEmptyError()
        self.remote().sudo.tee("/etc/hostname", _in=fqdn.split(".", 1)[0], _fg=True)

    def ensure_admin(
        self,
        username: str | None = None,
        authorized_keys: str | None = None,
        as_root: bool = False,
    ):
        username = username or self.admin
        self.ensure_user(username, as_root=as_root)
        self.ensure_authorized_keys(username, keys=authorized_keys, as_root=as_root)
        self.ensure_sudoer(username, as_root=as_root)

    def ensure_sudoer(
        self,
        username: Optional[str] = None,
        access: str = "ALL=(ALL) NOPASSWD:ALL",
        as_root: bool = False,
    ):
        conn = self.remote("root") if as_root else self.remote().sudo
        username = username or self.admin
        if not conn.ls(q(f"/etc/sudoers.d/{username}"), _ok_code=[0, 2]):
            conn.tee(
                q(f"/etc/sudoers.d/{username}"),
                _in=f"{username} {access}",
            )

            conn.chmod("0440", q(f"/etc/sudoers.d/{username}"))
        self.remote(username).sudo.echo("sudo setup successful", _fg=True)

    def ensure_user(
        self, username: str, shell: str = "/bin/bash", as_root: bool = False
    ):
        conn = self.remote("root") if as_root else self.remote().sudo
        if not conn.id(q(username), _ok_code=[0, 1]):
            conn.useradd("-m", "-s", q(shell), q(username), _fg=True)

    def ensure_users(self, users: dict[str, dict[str, str]] | None = None):
        for username, config in (users or self.users).items():
            self.ensure_user(username, **config, as_root=False)

    def ensure_authorized_keys(
        self, username: str, keys: str | None, as_root: bool = False
    ):
        conn = self.remote("root") if as_root else self.remote().sudo
        sshdir = f"/home/{username}/.ssh"
        dest = f"/{sshdir}/authorized_keys"
        conn.mkdir("-pv", q(sshdir), _fg=True)
        conn.tee(q(dest), _in=keys or self.authorized_keys)
        conn.chown("-R", q(f"{username}:{username}"), sshdir, _fg=True)
        conn.chmod("0600", dest, _fg=True)
        self.remote(login=username).echo(f"{username}: ssh setup successful", _fg=True)

    def disable_root_login(self):
        sudo_conn = self.remote().sudo
        if sudo_conn.grep(
            q("^PermitRootLogin\\syes"), "/etc/ssh/sshd_config", _ok_code=[0, 1]
        ):
            sudo_conn.sed("-i", "/^PermitRootLogin/s/yes/no/", "/etc/ssh/sshd_config")
            sudo_conn.systemctl.reload.ssh()
