import sys

from luamb._datadirs import ENVS_DIR


def main():
    # This part should execute as fast as possible so as not to slow down
    # shell startup. For this reason we do not use ArgumentParser here and
    # do not import anything on module level except for some standard modules.
    if len(sys.argv) == 2 and sys.argv[1] == 'shellsrc':
        import shlex

        from luamb._shell import shellsrc

        print(f'__luamb_envs_dir={shlex.quote(str(ENVS_DIR))}')
        print(shellsrc)
        sys.exit()

    def error(msg, exit_status=1):
        msg = '\033[0;31m{}\033[0m'.format(msg)
        print(msg, file=sys.stderr)
        sys.exit(exit_status)

    import os

    from ._exceptions import LuambException
    from ._hererocks import import_hererocks
    from ._luamb import Luamb

    luamb = Luamb(
        envs_dir=ENVS_DIR,
        active_env=os.environ.get('LUAMB_ACTIVE_ENV'),
        lua_default=os.environ.get('LUAMB_LUA_DEFAULT'),
        luarocks_default=os.environ.get('LUAMB_LUAROCKS_DEFAULT'),
        hererocks=import_hererocks(),
    )

    try:
        luamb.run()
    except LuambException as exc:
        error(exc)
