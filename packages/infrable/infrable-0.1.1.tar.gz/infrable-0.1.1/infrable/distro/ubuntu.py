from dataclasses import dataclass, field
from shlex import quote as q

from infrable.distro.linux import LinuxLatestHost


@dataclass(unsafe_hash=True, order=True, eq=True)
class UbuntuLatestHost(LinuxLatestHost):
    """A latest version of Ubuntu."""

    packages: list[str] = field(default_factory=list)

    def setup(self, as_root: bool = False):
        super().setup(as_root=as_root)
        self.upgrade_packages()
        self.update_packages()
        self.ensure_apt_packages()

    def upgrade_packages(self):
        self.remote().sudo(
            "apt-get", "-o", "DPkg::Lock::Timeout=60", "upgrade", "-y", _fg=True
        )

    def update_packages(self):
        self.remote().sudo(
            "apt-get", "-o", "DPkg::Lock::Timeout=60", "update", "-y", _fg=True
        )

    def ensure_apt_packages(self, packages: list[str] | None = None):
        packages = packages or self.packages
        if packages:
            self.remote().sudo(
                "apt-get", "-o", "DPkg::Lock::Timeout=60", "update", "-y", _fg=True
            )
            package_batches = [
                self.packages[i : i + 10] for i in range(0, len(packages), 10)
            ]
            for batch in package_batches:
                self.remote().sudo(
                    "apt-get",
                    "-o",
                    "DPkg::Lock::Timeout=60",
                    "install",
                    "-y",
                    *[q(pkg) for pkg in batch],
                    _fg=True,
                )
            self.remote().sudo(
                "apt-get", "-o", "DPkg::Lock::Timeout=60", "autoremove", "-y", _fg=True
            )

    def disable_root_login(self):
        sudo_conn = self.remote().sudo
        if sudo_conn.grep(
            q("^PermitRootLogin\\syes"), "/etc/ssh/sshd_config", _ok_code=[0, 1]
        ):
            sudo_conn.sed("-i", "/^PermitRootLogin/s/yes/no/", "/etc/ssh/sshd_config")
            sudo_conn.systemctl.reload.ssh()
