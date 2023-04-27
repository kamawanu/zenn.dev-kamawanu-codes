sudo sed -i.bak -e "/User=/s/jenkins/$USER/" /usr/lib/systemd/system/jenkins.service
sudo sed -i.bak -e "/ExecStart=/s/eval/eval nice/" /usr/lib/systemd/system/jenkins.service
sudo chown -R $USER /var/lib/jenkins /var/cache/jenkins
sudo systemctl daemon-reload
sudo systemctl restart jenkins
