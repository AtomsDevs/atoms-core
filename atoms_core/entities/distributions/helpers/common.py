import os
from pathlib import Path


class CommonDistribution:

    @staticmethod
    def set_current_user(chroot: str):
        '''
        Here we expose/fake the current user to the chroot and link its home
        directory to the chroot /home directory if it starts with /var/home as
        some distributions doen't do this by default.
        '''
        homedir = Path.home()
        chroot_homedir = os.path.join(chroot, "home", str(homedir.name))

        if not homedir.exists():
            # we have no access to the homedir, so nothing to do
            return

        if str(homedir).startswith("/var/home") and not os.path.exists(chroot_homedir):
            # the homedir is in /var/home, so we link it to the chroot
            # /home directory as explained above
            os.symlink(homedir, chroot_homedir)

        with open(os.path.join(chroot, "etc/passwd"), "a") as f:
            f.write(f"{os.getlogin()}:x:{os.getuid()}:{os.getgid()}::/home/{os.getlogin()}:\n")

        with open(os.path.join(chroot, "etc/group"), "a") as f:
            f.write(f"{os.getlogin()}:x:{os.getgid()}:{os.getlogin()}\n")
