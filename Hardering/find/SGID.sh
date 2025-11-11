sudo find / -executable -type f -perm -2000
sudo ls -lR / 2>/dev/null | grep -E '^-[rwx-]{5}[sS]'