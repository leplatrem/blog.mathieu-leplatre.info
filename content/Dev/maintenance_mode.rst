About Maintenance Mode
######################

You may be familiar with this situation: your team has been working on a project for a while, and now that it seems to do the job, it is not really justified for so many engineers to spend time on it.

Management agreed that the project should be switched to «maintenance mode». Even if the software remains critical and runs in production, the teams priorities have changed, and costs must be kept as low as possible.

From my experience, there is often some misunderstanding about turning a software into maintenance mode. If you continue to implement new features or spend time on refactoring internals, you are going to clash with your managers. If you don't touch the source at all and don't invest any engineering time at all, the software will soon qualify as «abandonware».

So, if the software still runs in production and is switched to maintenance, what should you expect to be done?

Monitor production
------------------

I remember one situation where a team used the origin server URL instead the CDN in their application, and went live. We suddenly received a massive amount of traffic, which caused the database to lag a lot, the application was then losing connections and crashing, users were seeing 503 error pages and reporting issues. Our first strategy had been to increase the database resources, which increased the costs of the service significantly.

Monitoring often seems like an obvious one. But it's not only about the server resources, it's mostly about making sure the software is just ticking over, handling load transparently, and not bothering you at night.

Make sure you have ways to monitor:

- **Load**: amount of traffic or activity
- **Responsiveness**: latency or lag
- **Robustness**: number of crash reports
- **Stability**: production issues tickets
- **Cost**: bills of cloud services

If these metrics become explicit and public, it gives everyone concrete goals to put or keep the application in its best conditions for the long run.

Optimize costs
--------------

Sometimes, a new system comes as a replacement, and the old one is maintained for legacy clients. Usually, the old system even becomes read-only. Nevertheless, it still relies on a database, some Web workers, executing domain specific code, with the sole purpose of serving static data for legacy clients! Some JSON files on a CDN could do the job!

If you know that you are going for the long run, it can be worth it to invest in optimizing the application. Even tiny parts.

Start with low hanging fruits, like slow queries, endpoints that serve static data, ...

Fix bugs
--------

No magic here, apart from the fact that some bug reports can actually be missing features in disguise.

Being able to fix bugs implicitly means that team members have a development setup on their machine, and that ideally running the software or its tests suite locally should not take several days.

Note that sometimes it can also be relevant to ignore some bugs, if their impact is minimal, their reproduction too complex, and the fix too fragile. They become «known bugs». Make sure you document them properly though.

Security patches
----------------

This one is interesting, because it means that you should keep your libraries and dependencies up-to-date.

It is highly recommended to automate this part with tools like `Dependabot <https://dependabot.com/>`_, `Renovate <https://renovatebot.com>`_ or `Snyk <https://snyk.io/>`_.

In our React application, keeping libraries up-to-date came out to be very costly. Indeed, the maintainers of the libraries were shipping security fixes in major releases with breaking changes, obliging us to rewrite some big parts of our app in order to keep up and benefit from security fixes.

In my opinion, it is very healthy for the team (and the project) to frequently touch the code and upgrade dependencies. It forces everyone to cherish the project, and most importantly: redeploy it regularly.

Redeploy regularly
------------------

This is extremely important: the team should be as confident as possible when redeploying the software.

Ideally, you have a setup with continuous deployment, at least on stage. Everytime a new version is tagged, the application is rolled out on some server.

If you wait too long between releases and deployments, you take the risk that some deployment recipe breaks, or becomes out of date, relying on missing resources or permissions.

Manage knowledge
----------------

When the whole team is working on the project daily, knowledge flows and is globally available. In maintenance mode, a couple of people are involved sporatically, and knowledge about procedures or technical details will evaporate quickly.

Plus, it is unfortunately very likely that, along the years, the members of the original team will have left the company.

An efficient way to make sure the project documentation is up-to-date is to give new hires the responsibility to update it as their first assignment :) For example, follow the procedure to setup their machine for development, and fix every step in docs where they got stuck.

In addition, exactly like planes or cars have their maintenance logs, it could be useful to keep a single document where every intervention is described.

When things turn sour, take the time to write down a *post-mortem*, that breaks down the timeline of events, the steps of troubleshooting, the lessons learnt, the improvements to be made, etc. This will become highly valuable for the future maintainers.

Open source contributions
-------------------------

Imagine the following situation: a company develops a software for a Web API, releases it as open source, and builds a community around it. After some time, the company's strategy (or goals) changes and the API is switch to maintenance mode, with lowest risks possible. The community continues to submit contributions for new features and risky refactors.

What should they do?

Ignore the contributions and kill the community?

Maintain their own fork with bug and security fixes only?

Make sure every new feature is behind a config flag?

Keep upgrading their API in production to the latest version?

I don't think there is a simple answer to this one. It truely depends on multiple factors, like the size of the community, the criticity of the API, the quality of contributions, etc.

Refusing pull requests is often very hard, but keep in mind that saying «no» can save everybody a lot of trouble.

Risk assessment
---------------

In toxic environments, engineers will sometimes blame each other for having failed to comply with certain expectations. In order to avoid that, some will work triple to reach what they see as *perfection*. Or when a top-down decision is made, they will disagree and disapprove their management, complaining that «they have no idea how reckless this is».

Of course, there are really bad managers out there, but I believe that the most common mistake is to keep your risks analysis for yourself.

No matter what the current situation is, and how far it is from being ideal, write down all potential risks explicitly and share them with the team.

The *Risk assessment* exercice consists in:

1. Identifying all potential catastrophic scenarios, incidents or deteriorations, in terms of stability, security, team motivation, whatever!
2. Evaluating likelihood, severity, and impact of each identified risk
3. Deciding which ones to ignore and why, and which ones that will have to be taken care of.

By making this list explicit and public, your long term maintenance strategy, whatever it is, is supported by a proper evaluation and awareness of risks.

Conclusion
----------

I really hesitated to write down this article. The more I was thinking about it, the more it feld like *Captain Obvious* was speaking.

At least, I hope that you enjoyed reading it! And in case everything sounded straightforward, please know that I enjoyed writing it, and kind of proud to have some perspective about these topics.

As usual, please don't hesitate to share your feedback or thoughts, I would be super happy to have a chat and/or integrate your contributions in the article!
