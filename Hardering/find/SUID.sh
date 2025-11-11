sudo find / -executable -type f -perm -4000
sudo ls -lR / 2>/dev/null | grep -E '^-[rwx-]{2}[sS]'