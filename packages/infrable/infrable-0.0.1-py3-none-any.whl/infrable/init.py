from pathlib import Path

INFRA_PY = """
import typer
from infrable import Host, Meta, Service, Switch, readfile

template_prefix = "https://github.com/username/repo/blob/main"


# Environments/ ----------------------------------------------------------------
dev = "dev"
beta = "beta"
prod = "prod"

environments = {dev, beta, prod}
env = Switch(environments, init=dev)
current_env = env()
# /Environments ----------------------------------------------------------------


# Hosts/ -----------------------------------------------------------------------
dev_host = Host(fqdn="dev.example.com", ip="127.0.0.1")
beta_host = Host(fqdn="beta.example.com", ip="127.0.0.1")
prod_host = Host(fqdn="prod.example.com", ip="127.0.0.1")

managed_hosts = env(
    dev=[dev_host],
    beta=[beta_host],
    prod=[prod_host],
)
# /Hosts -----------------------------------------------------------------------


# Services/ --------------------------------------------------------------------
web = Service(
    host=env(dev=dev_host, beta=beta_host, prod=prod_host),
    meta=Meta(secret_key=readfile("secrets/web/secret_key")),
    port=8080,
)

nginx = Service(
    port=80,
    host=env(dev=dev_host, beta=beta_host, prod=prod_host),
)
# /Services --------------------------------------------------------------------


# Tasks/ -----------------------------------------------------------------------
nginx.typer = typer.Typer()
@nginx.typer.command()
def reload(test: bool = True):
    assert nginx.host, "Service must have a host to reload"
    if test:
        nginx.host.remote().sudo.nginx("-t")
    nginx.host.remote().sudo.systemctl.reload.nginx()

@nginx.typer.command()
def restart(test: bool = True):
    assert nginx.host, "Service must have a host to restart"
    if test:
        nginx.host.remote().sudo.nginx("-t")
    nginx.host.remote().sudo.systemctl.restart.nginx()
""".strip()

NGINX_PROXY_PARAMS_TEMPLATE = """
# vim: syn=nginx

# ---
# src: {{ template_prefix }}/{{ _template.src }}
# dest:
# {% for host in managed_hosts %}
#   - loc: {{ host }}:/etc/nginx/proxy_params
# {% endfor %}
# chmod: 644
# chown: root:root
# ---
proxy_set_header Host $http_host;
proxy_set_header X-Real-IP $remote_addr;
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
proxy_set_header X-Forwarded-Proto $scheme;
""".strip()

NGINX_WEB_TEMPLATE = """
# vim: syn=nginx

# ---
# src: {{ template_prefix }}/{{ _template.src }}
# dest: {{ nginx.host }}:/etc/nginx/sites-enabled/web
# chmod: 644
# chown: root:root
# ---

server {
    listen 80;
    listen [::]:80;

    server_name {{ nginx.host.fqdn }} www.{{ nginx.host.fqdn }};

    location / {
        proxy_pass http://localhost:{{ web.port }};
        include proxy_params;
    }
}
""".strip()

FILES = {
    "infra.py": INFRA_PY,
    "templates/nginx/proxy_params.j2": NGINX_PROXY_PARAMS_TEMPLATE,
    "templates/nginx/web.j2": NGINX_WEB_TEMPLATE,
}


def init():
    for filename, content in FILES.items():
        path = Path(filename)
        if path.exists() and path.read_text().strip():
            print(f"Skipping {path}, Exists.")
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
        print(f"Created {path}.")
