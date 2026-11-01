---
title: "Super Simple Node.js Continuous Deployment using SaltStack and systemd"
description: "I'm a big fan of the SaltStack configuration management system. It's an extremely flexible and powerful system, but is also quite easy to use. When I initially set up this new rele"
pubDate: "2016-09-12"
tags: ["saltstack", development]
archived: true
---

I'm a big fan of the **[SaltStack](https://docs.saltstack.com/)** configuration management system. It's an extremely flexible and powerful system, but is also quite easy to use. When I initially set up this new release of this website, I had done most of the configuration manually. Not that it's a particularly complex operation, two Node apps and nginx proxying those sites. I used [forever](https://www.npmjs.com/package/forever) to keep those two sites running.

Since that initial deploy, I've gained more exposure to the **systemd** platform (and learned that just calling it an init system is probably a good way to get called out online). Despite the criticism it receives, I think that as an init system, it is a great improvement over previous systems like Upstart. In fact, when it comes to defining new services, I think it shares the same adjectives I used to describe SaltStack in the opening sentence of this post - flexible, powerful, and easy to use! 

Besides easy creation and management of services, running Node apps via systemd offers some other benefits, like powerful integrated logging via journald and a simple-to-use dependency system (so you can ensure your Redis database is running when your web app goes to start). [This article](https://blog.codeship.com/running-node-js-linux-systemd/) from Codeship offers more insight into running your Node app using systemd services.

---
So say you now have one or more `.service` units you want to deploy on your server. Before you go ahead and clone your repository by hand, have you considered how easy it is to build a continuous deployment system to automatically deploy the latest version of your code?

When you break down the problem of installing and running the latest version of your Node app, it involves these steps:

1. Check out the latest source code from whatever branch you want to deploy
2. `npm install` to install any required dependencies
3. `npm start` or otherwise start your application

Sounds like an easy process for a configuration management system like Salt to handle! Salt uses "states" to configure your system so that it ends up matching a desired state (hence the name). To deploy this figurative node app, you can have a state as simple as this:

    # (1)
    /var/sites/mynodeapp:
      file.directory: []

    # (2)
    mynodeapp-repo:
      git.latest:
        - name: git@github.com:hello/mynodeapp.git
        - branch: master
        - target: /var/sites/mynodeapp
        - require:
          - file: /var/sites/mynodeapp

    # (3)
    mynodeapp-npm-install:
      cmd.wait:
        - name: 'npm install'
        - cwd: /var/sites/mynodeapp
        - watch:
          - git: mynodeapp-repo

    # (4)
    /etc/systemd/system/node-mynodeapp.service:
      file.managed:
        - contents: |
          [Unit]
          After=network.target

          [Service]
          ExecStart=/usr/local/bin/npm start
          WorkingDirectory=/var/sites/mynodeapp
          Restart=always
          Environment=NODE_ENV=production

          [Install]
          WantedBy=multi-user.target

    # (5)
    node-mynodeapp-daemon-reload:
      module.run:
        - name: service.systemctl_reload
        - watch:
          - file: /etc/systemd/system/node-mynodeapp.service

    # (6)
    node-mynodeapp-service:
      service.running:
        - name: node-mynodeapp
        - enable: True
        - watch:
          - git: mynodeapp-repo
          - file: /etc/systemd/system/node-mynodeapp.service

A less than 50-line config file is all that is needed to install and run your application! For a breakdown for what each of these blocks do, read on:

1. Creates a directory to host your application in
2. Ensure the specified git repository is cloned or up to date with the upstream repository in the `target` directory specified.
3. Run the `npm install` command in the application directory. Pairing the wait function with the **watch** directive, this command will only be run when the git state changes (i.e. a new commit is pulled down)
4. Define the systemd `.service` unit file for this application and install it in the proper location.
5. In Salt's systemd module, there is a specific function that will run `systemctl daemon-reload`. We add a wait condition here to only run this state when the .service file changes (no need to always reload). This step also demonstrates an extremely useful feature of SaltStack - states can call execution modules (modules are functions usually called right from the salt command line), and modules can call states. Being able to cross-call means even if no state exists in Salt to do what you want (like in this case), you can just call the module and still get all the benefits of a state like require or watch directives.
6. Finally, this state ensures the named service is running.  `enable: True` ensures the service starts on system boot. As you can see, you can provide multiple watch conditions. In this case, when either the git repository is updated or the .service file is updated, *the service will be restarted*.

If you save the above file as "mynodeapp.sls" in `/srv/salt`, you can run `salt-call --local state.sls mynodeapp` and the latest version of your app will be downloaded, installed, and run. Make a change to your source code? Just run that command again and Salt will git pull the changes, install any new dependencies from npm and restart your application! Simple as that!

If you have multiple applications you want to run, make multiple .sls files, add the name of those files to your [top file](https://docs.saltstack.com/en/latest/ref/states/top.html) and run the `state.highstate` function. Presto, you just updated all of your apps at once!

Hopefully this demonstrates how easy it is to set up a continuous deployment solution using SaltStack. It took me only a couple hours one evening last week to test and upgrade my site to automate configuration of my site. 

If you want to take this technique to the next level, know that Salt has a REST API you can enable to execute commands remotely via HTTP calls. We'll save a more thorough discussion of that for another time, though.

*Note: While I described setting up a Node.js application in this blog post because that's what I did to set to configure this website, the steps should apply to any language/framework that works in a similar way, like Python or Ruby*

