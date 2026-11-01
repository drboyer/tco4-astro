---
title: "Welcome to the new thecloudonline.net!"
description: "As seems to always be the case when it comes to my personal website, it was a bit of a journey to get to this newly-relaunched site. Real life gets complicated - there are certainl"
pubDate: "2016-06-11"
tags: ["Site Updates"]
archived: true
image: "/images/tco3-homepage.png"
---

As seems to always be the case when it comes to my personal website, it was a bit of a journey to get to this newly-relaunched site. Real life gets complicated - there are certainly many days when after spending a full workday solving programming problems, there's just not much energy to jump right back into "creation" mode. Whether that means designing the site or blogging. Hopefully I can at least make more of an effort on the latter part going forward now that the programming work is mostly settled!

I've owned thecloudonline.net since 2010 (right before graduating high school) but have maintained a site under that "name" since a few years before that. The original site featured an actual weekly forecast page I would write for my hometown, in addition to weather related articles (relevant for high schoolers, like "Are we going to get a snow day?").
![Old forecast](/blog/content/images/2016/06/old-fcst.PNG)

In 2010, I relaunched the site and dropped the forecast section (I did link to the new home for my forecasts, the Penn State [Campus Weather Service](http://www.campusweatherservice.com/). I wrote a handful of articles over the years about different, mostly weather-related, topics which have been "reprinted" here.

As I'm now into my career as a software engineer, but very much proud to call myself a meteorologist, I wanted to pivot this site to add perhaps a more "technological" angle to it. I'm a big fan of open source software and hope to perhaps write about that some more in the future, like various projects I'm working on. And hopefully add some more weather-related content as well. So stay tuned, hopefully you'll find interesting posts here - past, present, and future!

---

## Technical Details

*I broke this section out to only those interested in a more technical discussion.* As mentioned above, this is the third "major" version of thecloudonline.net. Throughout the relaunch project, I had these major goals:

* Explore **node.js** as a platform for web development
* Give the site a modern, **responsive theme** (so you can read all my exciting stories on the go, haha)
* After reading about the [**Let's Encrypt** project](https://letsencrypt.org/), I wanted to implement HTTPS on my site

I've been able to accomplish all 3 of these goals. This site has gone, over the years, from a custom HTML site with a little bit of PHP, to a Drupal site with a custom theme, to a Wordpress site temporarily (*never again!*), and finally to a custom site again using the Express node framework, [Ghost](https://ghost.org) blogging platform, and nginx as a reverse proxy. So I feel like, in a sense, I've almost come full circle, back to a more custom platform. I like it.

The new site is themed with a "Material Design" Bootstrap theme. I really like the Material Design look, especially as a long-time Android user. There are some plans in my head to iterate the site design a bit more and perhaps incorporate even a bit more Material look and feel into it.

Finally, I'm really excited to have gotten Let's Encrypt up and running. I think it's a great project to make it easy to get any site running HTTPS with free certificates. It's lowered the entry cost to improved site security quite a bit, even time wise if you follow [handy guides](https://www.digitalocean.com/community/tutorials/how-to-secure-nginx-with-let-s-encrypt-on-ubuntu-14-04) like I did to get it set up in an automated fashion!
