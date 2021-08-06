About Maintenance Mode
######################

:tags: tips, methodology
:date: 2021-08-04

You may be familiar with this situation: your team has been working on a project for a while, and now that it seems to do the job, it is not really justified for so many engineers to spend time on it.

Management agreed that the project should be switched to «maintenance mode». Even if the software remains critical and runs in production, the team's priorities have changed, and costs must be kept as low as possible.

From my experience, there is often some misunderstanding about turning a software into maintenance mode. If you continue to implement new features or spend time on refactoring internals, you are going to clash with your managers. If you don't touch the source at all and don't invest any engineering time at all, the software will soon qualify as «abandonware».

So, if the software still runs in production and is switched to maintenance, what should you expect to be done?

.. figure:: {static}/images/maintenance-nasa.jpg
    :alt: NASA Engine Maintenance Training CC-BY-NC https://www.flickr.com/photos/nasa2explore/49243482926/
    :align: center

    NASA Engine Maintenance Training `CC-NC-ND <https://www.flickr.com/photos/nasa2explore/49243482926/>`_

Monitor production
------------------

I remember one situation where a team used the URL of the origin server for our service instead of the CDN. And went live. We suddenly received a massive amount of traffic, which caused the database to lag a lot, the application was then losing connections and crashing, users were seeing 503 error pages and reporting issues. Our first strategy had been to increase the database resources, which increased the costs of the service significantly.

Monitoring often seems like an obvious one. But it's not only about the server resources, it's mostly about making sure the software is just ticking over, handling load transparently, and not bothering you at night.

Make sure you have ways to monitor:

- **Load**: amount of traffic or activity
- **Responsiveness**: latency or lag
- **Robustness**: number of crash reports
- **Stability**: production issues tickets
- **Cost**: bills of cloud services

If these metrics become explicit and public, it gives everyone concrete and measurable goals to put the application in its best conditions for the long run.

Optimize costs
--------------

Sometimes, a new system comes as a replacement, and the old one is maintained for legacy clients. Usually, the old system even becomes read-only. Nevertheless, it still relies on a database, some Web workers, executing domain specific code, with the sole purpose of serving static data for legacy clients! Some JSON files on a CDN could do the job!

If you know that you are going for the long run, investing in optimization can be worth it. Even tiny parts.

Of course, it is imperative to evaluate how much you can save per month/year before investing efforts! Beware of rabbit holes, always timebox your work! Start with low hanging fruits, like slow queries, endpoints that serve static data, ...

If your infrastructure allows it, you could also leverage some of the auto-scaling features of your cloud provider. For example, at Mozilla, we clearly have pattern of loads depending of time and day of the week. Setting up rules to scale up/out or in/down your resources can help you save money. Combined with proper monitoring and metrics, it can truly be rewarding.

Fix bugs
--------

No magic here, apart from the fact that some bug reports can actually be missing features in disguise.

Being able to fix bugs implicitly means that team members have a development setup on their machine. Ideally, running the software or its tests suite locally should not take several days.

Note that sometimes it can also be relevant to ignore some bugs, if their impact is minimal, their reproduction too complex, and the fix too fragile. They become «known bugs». Make sure you document them properly though.

Counterintuitively, fixing bugs and polishing rough edges can be entertaining. Some people are suited for maintenance (fixers!), others prefer innovation (builders!), but having experienced both perspectives is precious.

Apply security patches
----------------------

This one is interesting, because it means that you should keep your libraries and dependencies up-to-date.

It is highly recommended to automate this part with tools like `Dependabot <https://dependabot.com/>`_, `Renovate <https://renovatebot.com>`_ or `Snyk <https://snyk.io/>`_.

In our React application, keeping libraries up-to-date came out to be very costly. Indeed, the maintainers of the libraries were shipping security fixes in major releases with breaking changes, obliging us to rewrite some big parts of our app in order to keep up and benefit from security fixes.

In my opinion, it is very healthy for the team (and the project) to frequently touch the code and upgrade dependencies. It forces everyone to cherish the project, and most importantly: redeploy it regularly.

Redeploy regularly
------------------

This one is extremely important: the team should be as confident as possible when redeploying the software.

In a perfect world, you have a setup with continuous deployment, at least on stage. Everytime a new version is tagged, the application is rolled out on some server.

If you wait too long between releases and deployments, you take the risk that some deployment recipe breaks, or becomes out of date, relying on missing resources or permissions.

.. figure:: {static}/images/maintenance-plane.jpg
    :alt: Aviation Machinist conducts maintenance on an afterburner CC-BY-NC https://www.flickr.com/photos/compacflt/51319755467/
    :align: center

    Aviation Machinist conducts maintenance on an afterburner `CC-BY-NC <https://www.flickr.com/photos/compacflt/51319755467/>`_

Sustain Infrastructure
----------------------

If your application uses some cloud provider's services, you will also have to keep afloat with upgrades and decommissions. If your application is not compatible with the only versions available, some code ought to be rewritten.

For example, Amazon regularly rolls out new versions of PostgreSQL, and cojointly shutdowns old versions.

Exactly like for your software libraries, part of a Kubernetes cluster lifecycle involves performing periodic upgrades to the latest version, in order to apply the latest security releases. Automation is possible but can also give you surprises!

On top of that, your company can also decide to migrate its whole infrastructure to a different cloud provider. That may require some code to be rewritten (eg. Amazon S3 versus Google Cloud Storage) and very likely critical parts.

Manage Knowledge
----------------

When the whole team is working on the project daily, knowledge flows and is globally available. In maintenance mode, a couple of people are involved sporadically, and knowledge about procedures or technical details will evaporate quickly.

Plus, it is unfortunately very likely that, along the years, the members of the original team will have left the company.

An efficient way to make sure the project documentation is up-to-date is to give new hires the responsibility to update it as their first assignment :) For example, they will follow the procedure to setup their machine for development, and fix every step in docs where they got stuck.

In addition, exactly like planes or cars have their maintenance logs, it could be useful to keep a single document where every intervention in production is described.

When things turn sour, take the time to write down a *post-mortem*, that breaks down the timeline of events, the steps of troubleshooting, the lessons learnt, the improvements to be made, etc. This will become highly valuable for the future maintainers.

.. figure:: {static}/images/maintenance-classic-programmer.jpg
    :alt: https://classicprogrammerpaintings.com/post/143947399671/developers-look-for-documentation-in-legacy
    :align: center

    Developers look for documentation in legacy system - Jean-François Millet, 1857 - Oil on canvas (by `classic programmer paintings <https://classicprogrammerpaintings.com/post/143947399671/developers-look-for-documentation-in-legacy>`_)


Handle Open source Contributions
--------------------------------

Imagine the following situation: a company develops a software for a Web API, releases it as open source, and builds a community around it. After some time, the company's strategy (or goals) changes and the API is switched to maintenance mode, with lowest risks possible. The community continues to submit contributions for new features and risky refactors.

What should the company do?

Ignore the contributions and kill the community?

Maintain its own fork with bug and security fixes only?

Make sure every new feature is behind a config flag?

Keep upgrading their API in production to the latest version?

I don't think there is a simple answer to this one. It truly depends on multiple factors, like the size of the community, the criticality of the API, the quality of contributions, etc.

Refusing pull requests is often very hard, but keep in mind that saying «no» can save everybody a lot of trouble.

Assess Risks
------------

You may not have enough resources to complete all of the above successfully. Maintenance of complex software is hard. And shit happens. Think of your software as an old building open to the public, it is your responsability to report any potential danger that you see.

In toxic environments, engineers will sometimes blame each other for having failed to comply with certain expectations. In order to avoid that, some will work triple to reach what they see as *perfection*. Or when a top-down decision is made, they will disagree and disapprove of their management, complaining that «they have no idea how reckless this is».

Of course, there are really bad managers out there, but I believe that the most common mistake is to keep your risk analysis for yourself.

No matter what the current situation is, and how far it is from being ideal, write down all potential risks explicitly and share them with the team.

The *Risk Assessment* exercice consists in:

1. Identifying all potential catastrophic scenarios, incidents or deteriorations, in terms of stability, security, team motivation, whatever!
2. Evaluating likelihood, severity, and impact of each identified risk
3. Deciding which ones to ignore and why, and which ones that will have to be taken care of.

By making this list explicit and public, your long-term maintenance strategy, whatever it is, is supported by a proper evaluation and awareness of risks.

Conclusion
----------

If executives think that switching a project to *maintenance mode* will save a lot of money and effort, you now have some arguments to contrast their idea.

Maintenance cost is probably less than investing in new features, but it is definitely not zero.

Shutting down a service is also an option, leaving consumers in despair.

With the amount of connected devices that depend on closed-source Web APIs out there, I believe that long-term maintenance is going to become a major concern in the next years...

------

Many thanks to `Nico <https://nl.linkedin.com/in/nicolas-metaye-27766633>`_, `John <https://www.linkedin.com/in/johnwhitlock>`_, `Benson <https://www.linkedin.com/in/mostlygeek>`_, `Stephen <http://stephenhood.com>`_, `Sven <https://www.linkedin.com/in/smarnach/>`_, and `Areski <http://areskibelaid.com/>`_ for your precious feedback and suggestions!

As usual, please don't hesitate to share your feedback or thoughts, I would be super happy to have a chat and/or integrate your contributions in the article!
