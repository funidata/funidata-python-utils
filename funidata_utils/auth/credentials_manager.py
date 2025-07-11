#  Copyright (c) 2025 Funidata Oy.
#  All rights reserved.
# ------------------------------------------------------------------------------

from pathlib import Path

from .sis_credentials import SisuSettings


def get_sis_settings(
    environments_dir: Path | str,
    environment: str | None = None,
) -> SisuSettings:
    if isinstance(environments_dir, str):
        environments_dir = Path(environments_dir)

    if not environments_dir.exists() or not environments_dir.is_dir():
        raise NotADirectoryError("environments_dir does not exist or is not a directory")

    if not environment:
        env_files = [x for x in environments_dir.iterdir() if x.is_file() and x.suffix == '.env']
        if len(env_files) == 1:
            environment = env_files[0].stem
        else:
            environment = input(f"Which environment? {[x.stem for x in env_files]}\n")

    proxies_port = input('Give proxy port (leaving this empty will default this value to null): ') or None
    proxies = {
        'http': f'socks5://127.0.0.1:{proxies_port}',
        'https': f'socks5://127.0.0.1:{proxies_port}'
    } if proxies_port else None

    return SisuSettings(_env_file=f'{environments_dir}/{environment}.env', socks_proxies=proxies)  # noqa
