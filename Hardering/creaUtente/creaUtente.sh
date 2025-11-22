sudo useradd -m -s /bin/bash utente1DayPsw
sudo echo 'utente1DayPsw:utente1DayPsw' | sudo chpasswd
sudo chage -M 1 utente1DayPsw
sudo chage -W 1 utente1DayPsw
sudo chage -l utente1DayPsw