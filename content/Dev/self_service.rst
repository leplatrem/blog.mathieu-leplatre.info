About Self-Service
##################

:tags: tips, methodology
:date: 2024-07-08

When I hear *self-service*, I think of a restaurant where customers serve themselves, which minimizes wait times and maximizes efficiency. Similarly, in our software engineering team, self-service solutions empower other teams to get what they need without waiting for our assistance, leading to faster service and reduced context switching.

Let's explore what self-service means in our domain and how different approaches can be implemented to achieve it.


Redefining Self-Service in Software Teams
-----------------------------------------

.. figure:: {static}/images/self_service-self-service.webp
    :alt: Image generated by OpenAI's DALL-E model - A Pixar-style senior engineer character interacting with a self-service machine at a fast food restaurant.
    :align: center
    :width: 70%

What is not self-service? 

1. I need something
2. I open a ticket
3. The ticket is put in a backlog
4. One or a few operators handle it
5. I receive what I asked

This is the usual experience at fast-foods. Latency at *Step 4* being reduced to its maximum with a lot of coordination and pressure on workers.

In companies, you're very likely to face this process too, because only a few administrators have the necessary privileges to get you what you want. 

Believe it or not, but I've seen projects where onboarding a new instance of a resource consisted in waiting for engineers to modify the source code and then operators to redeploy the service and migrate the database schema. Days of work. Mostly coordination latency.

It may seem obvious, but ideally this is what we want:

1. I need something
2. I follow step-by-step instructions
3. I receive it

Between *Step 2* and *Step 3*, there could be an additional approval step, which at most consists in a single action to reject or accept the request.  

In practice, self-service is not so obvious to implement, but the benefits are clear.


Level 0: Empowerment Through Knowledge
--------------------------------------

.. figure:: {static}/images/self_service-documentation.webp
    :alt: Image generated by OpenAI's DALL-E model - A Pixar-style senior engineer character reading a big book in a library.
    :align: center
    :width: 70%

This is like level 0 of self service. RTFD.

All procedures are documented in a company wiki, using FAQs, tutorials, cookbooks, in order to empower employees to find answers on their own.

If the documentation repository is very well-maintained and organized, it would globally work. But from my experience, content is usually outdated and hard to find. Searching via keywords on Confluence is clearly not a panacea. It takes a real job (archivist or filing clerk) to build good documentation.

AI and specialized language models can significantly improve searchability and relevance of information, making it easier for employees to find what they need quickly.

- **Cost**: ⭐️⭐️⭐️⭐️ ☆
- **Productivity**: ⭐️ ☆ ☆ ☆ ☆


GUI: Bridging the Gap for Non-Technical Users
---------------------------------------------

.. figure:: {static}/images/self_service-gui.webp
    :alt: Image generated by OpenAI's DALL-E model - A Pixar-style senior engineer character using a shiny iMac computer.
    :align: center
    :width: 70%

At the other side of the spectrum: user interfaces. 

You build a (Web) UI where users can login, view and edit resources, submit their request, and obtain or wait for the result.

These user interfaces are extremely expensive to build:

- Intuitive design and user experience are crucial and too easy to get wrong;
- UI must adapt to users privileges;
- Likely to reinvent the wheel for review and approval workflows, comments and request status updates; 
- Web apps are toilsome to build and maintain (anyone maintaining a JS project with a dozen of dependencies knows that);

They make sense if a lot of users interact very often with them, especially if they are non-technical, but in some situations they will generally cost a lot more than the value they bring. Bad user interfaces can also be very frustrating and counterproductive.

- **Cost**: ⭐️⭐️⭐️⭐️⭐️
- **Productivity**: ⭐️⭐️⭐️⭐️⭐️


APIs: The Backbone of Autonomous Teams
--------------------------------------

.. figure:: {static}/images/self_service-apis.webp
    :alt: Image generated by OpenAI's DALL-E model - A Pixar-style senior engineer character building a bridge.
    :align: center
    :width: 70%

Around 2002, Jeff Bezos told his employees to build APIs in order to enable teams to independently access and utilize each other's services without needing direct inter-team communication or coordination.

You need a database in prod? Just call the API to get it, ``POST /databases/prod/mydb``!

This is a great idea, that served as the foundations of AWS, and was probably one of the keystones to the company success. 

But concretely, how many companies did implement this concretely? Unless you're working at Google or Amazon, it's very likely that if you need a new sub-domain name for your app, you'll have to fill a Jira ticket 😏

This approach requires excellent documentation and API versioning. And I don't know how offering self service APIs would work for non-technical employees, for which it may not be obvious to perform tasks programmatically.

- **Cost**: ⭐️⭐️⭐️ ☆ ☆
- **Productivity**: ⭐️⭐️ ☆ ☆ ☆


Efficient Interactions with Chat Bots
-------------------------------------

.. figure:: {static}/images/self_service-chatbots.webp
    :alt: Image generated by OpenAI's DALL-E model - A Pixar-style senior engineer character handshaking a droid. 
    :align: center
    :width: 70%

In my daily life, I generally hate chat bots that pretend to be human. The other day, I received a WhatsApp bot message with some health insurance details for someone else. Apparently, this person's phone number had a typo, and I did my best to tell the remote machine that I had nothing to do with this, but there was no way—it was not programmed for this situation apparently.

However, I find them extremely useful and handy when their dialogue interface is a finite list of commands.

In the context of self-service, we don't really need natural language. A list of possible operations and available options is a lot more efficient than a very bad imitation of a human waiter or a free text input box without guidance.

Chat bots can walk us through a step-by-step journey, and would perfectly replace typical `multi-step forms <https://en.wikipedia.org/wiki/Wizard_(software)>`_. 

Beyond basic Slack plugins and commands, I don't have too much experience with chat bots at work. I think we should do more with them, because compared to user interfaces, they are fairly easy and cheap to build.
I did `one <https://github.com/leplatrem/ihatemoney-bot>`_ for Telegram years ago using a high level SDK, and it was fun to implement!

- **Cost**: ⭐️⭐️⭐️ ☆ ☆
- **Productivity**: ⭐️⭐️⭐️⭐️ ☆


Files-Driven Workflows: Automation through CI/CD
------------------------------------------------

.. figure:: {static}/images/self_service-files-driven.webp
    :alt: Image generated by OpenAI's DALL-E model - A Pixar-style senior engineer character installing a machine that has gears. 
    :align: center
    :width: 70%

This has been my favorite in the last years: files on a Git repository with a CI/CD pipeline.

1. You open a pull-request on a Git repository to make changes
2. An automated job verifies that they look sound
3. A human approves it
4. An automated job executes the pipeline, and you see the results immediately

CI/CD scripts are relatively cheap to implement, and platforms like Gitlab or Github are straightforward to work with.

The level of abstraction is what matters here. The CI/CD pipeline does not always have to be super smart. For example, the files can be mounted directly in the containers and read when the application starts. Or a script can read the files and execute calls on APIs each time they are modified. I personally like when the files are flat and easy to reason about, and it's not always the case with *configuration as code* where resources are sometimes spread in tiny YAML files.

Permissions management and security are also main concerns. If you give the power to make changes to your infrastructure to a CI/CD worker, you better make sure to have good management of secrets and fine access control (VPN, user groups, ...).

Extensive linting is also highly recommended. A typo in a file, and you can end up replacing a resource with another without noticing! You can set up advanced solutions to execute dry runs or deploy temporary instances to give the reviewers better insights and more confidence in approving the changes.

This approach has some limits if a lot of employees have to modify the same set of files (merge conflicts!), but there are workarounds, and in most cases, the frequency of changes to the same resource remains relatively low.

- **Cost**: ⭐️⭐️⭐️ ☆ ☆
- **Productivity**: ⭐️⭐️⭐️⭐️ ☆


Do Less, Accomplish More
------------------------

.. figure:: {static}/images/self_service-conclusion.webp
    :alt: Image generated by OpenAI's DALL-E model - A Pixar-style senior engineer character laying back and relaxing, surrounded by his cheerful team of young engineers. 
    :align: center
    :width: 70%

Implementing self-service solutions can transform how your teams operate, leading to greater efficiency, reduced wait times, and more satisfied employees. As shown in this article, there are many possible alternatives before investing a lot of resources in building complex web user interfaces. Start small, iterate, and blend different approaches to create a self-service environment that not only empowers users but also allows your team to focus on high-impact tasks.

------

*You may have noticed that the English in this article is somewhat better than in other articles on this website. This is because I used GenAI (ChatGPT 4o to name it) for proofreading and corrections, and, as you may have guessed, for illustrations too. It doesn't mean I'll always use it in the future. I hope it didn't affect the reading experience too much.*
