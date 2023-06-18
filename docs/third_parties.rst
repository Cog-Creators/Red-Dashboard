.. Third Parties

.. role:: python(code)
    :language: python

=============
Third Parties
=============

This guide will cover how Red-Dashboard works with third parties and how cog creators can add their own pages to the web dashboard.

---------------
Getting Started
---------------

Red-Dashboard supports third party integration, which means that cog creators can add pages to Red-Dashboard with their cogs.
An end user will not have to do anything, just install and load the cogs that do it on their dashboard bound bot.

A "Third Parties" page has been added to the side menu of the dashboard, where you can easily access the pages that are not hidden. The hidden pages will be accessible with a link given by the cog itself.

Third parties are not an integral part of Red-Dashboard. Any information you provide will be used by them, not Red-Dashboard or the cog Dashboard.
For more information: https://github.com/Cog-Creators/Red-Dashboard/blob/master/documents/Third%20Party%20Disclaimer.md

-------------------
How does that work?
-------------------

If you are an end user, you do not need to continue reading this document, unless you want to understand how the third parts work. If you are a cog creator who wants to integrate Red-Dashboard with your cogs, you can read on.

On the Red-Dashboard side:
--------------------------

An API endpoint point has been added: `/third_party/<cog_name>/[page]?**[params]`.
The local Dashboard cog sends the list of third parties and pages to Red-Dashboard, in the `get_variables` RPC method, which is already called at regular intervals. Thus, the code checks if the cog, and the page exist.

Depending on the parameters provided by the cogs creator, the code will deny requests if the method used is not one of the allowed ones (`HEAD`, `GET`, `OPTIONS`, `POST`, `PATH` and `DELETE`). If `user_id` is a required parameter, then the Dashboard will request the OAuth login of the current user. If `guild_id` is required, then the current `dashboard.html` page will be displayed to allow the choice of a server.

`user_id`, `guild_id`, `member_id`, `role_id` and `channel_id` are context variables, which should be integers: at the moment, choice is not possible for members, roles and channels, but these parameters could be provided by cogs manually in Discord. If parameters are required, the Dashboard will display an error on the browser.

A web request will be sent to the local cog Dashboard which will dispatch the data correctly and get a response.

Types of responses from third parties:
--------------------------------------

The third parties must return to the local cog Dashboard a `dict` like a real RPC method would.

Several keys are supported by the API endpoint:

- `status`: Any request response should have it, but it is not used.

- `web-content`: The Flask/Django/Jinja2 template will be displayed on the browser. It can contain HTML, CSS and JavaScript, and should start with `{% extends "base-site.html" %}` to display the base dashboard layout. The variables in the response will be passed in.

- `error_message`: Using the html file `error_message.html`, the provided message will be displayed directly to the user, without having to code a different html content.

- `redirect`: The existing template with its name will be displayed. The variables of the response will be passed on.

If content fields are not passed on, or if the request methods are other than `HEAD` and `GET`, the data will be returned directly as JSON.

On the Dashboard local cog side:
--------------------------------

A `DashboardRPC_ThirdParties` extension has been added and is accessible at `Dashboard.rpc.third_parties_handler`. A third party is linked to a `commands.Cog` object which must be loaded, in order to be used.
The `DashboardRPC_ThirdParties.add_third_party` method must be used to add a cog as a third party.  The page parameters are stored in `DashboardRPC_ThirdParties.third_parties`.

The decorator `dashboard.rpc.thirdparties.dashboard_page` allows to provide parameters for each page. All attributes of the cog class that have a `__dashboard_params__` attribute will be automatically added to the Dashboard when the add third party method is called. Context parameters (`user_id`/`user`, `guild_id`/`guild`, `member_id`/`member`, `role_id`/`role`, `channel_id`/`channel`) and required parameters are detected in the method parameters names.

Here are its parameters:

- `name` (`Optional[str]`): `None` so that the user does not have to specify the name to get this page. A name will have the same limitations as the Discord slash command names for ease of use.

- `methods` (`List[Literal["HEAD", "GET", "OPTIONS", "POST", "PATCH", "DELETE"]]`): The web request methods allowed to call the third party page.

- `context_ids` (`List[str]`): To manually specify required context ids.

- `required_kwargs` (`List[str]`): To manually specify required parameters.

- `permissions_required` (`List[Literal["view", "botsettings", "permissions"]]`): The user's required permissions on the server.

- `hidden` (`bool`): A parameter not used at this time. Maybe the pages will be listed somewhere someday. Defaults is `False`, or `True` if there are required kwargs.

The RPC method `DashboardRPC_ThirdParties.data_receive` receives the data from Red-Dashboard for the endpoint API I mentioned earlier. In case, the existence of the third party and the page is checked at new.
If the cog is no longer loaded, the request is "refused" with an error message. If a `context_ids` variable is provided (`user_id`, `guild_id`, `member_id`, `role_id` or `channel_id`), the code checks if the bot has access to it and if the Discord objects really exist.
The parameters `user`, `guild`, `member`, `role` and `channel` are then added eventually.

The parameters received from the Red-Dashboard (and passed to cogs) are `method`, `**context_ids`, `**kwargs` and `lang_code`.
Cogs should use `**kwargs` last, as the user (or Flask) is free to add whatever parameters they wish to the pages in the URL.

--------------------------------------------
How to integrate third parties in your cogs?
--------------------------------------------

The cog Dashboard can be loaded after the third games when the bot is started or simply reloaded.
When loaded, it will trigger the `on_dashboard_cog_load` event. When a cog is loaded, it will manually call this event, only for the cog.
With this way, the cog can be added to Red-Dashboard in any condition, with only one method in addition to the pages.

To avoid having to use the `commands.Cog.cog_unload` method, the cog Dashboard uses the event in Red 3.5 `on_cog_remove` to remove the third party automatically on unloading.

Let's imagine a MyCog cog with Python files `__init__.py`, `mycog.py` and `dashboard_integration.py`.

In `__init__.py`:

.. code-block:: python

    from redbot.core.bot import Red

    from .mycog import MyCog

    async def setup(bot: Red):
        cog = MyCog(bot)
        await bot.add_cog(cog)

In `mycog.py`:

.. code-block:: python

    from redbot.core import commands
    from redbot.core.bot import Red

    class MyCog(DashboardIntegration, commands.Cog):  # Subclass `DashboardIntegration`: this allows to integrate the methods in the cog class, without overloading it.
        def __init__(self, bot: Red):
            self.bot: Red = bot

        @commands.command()
        async def hello(self, ctx: commands.Context):
            await ctx.send("Hello World!")

In `dashboard_integration.py`:

.. code-block:: python

    from redbot.core import commands
    from redbot.core.bot import Red
    import discord
    import typing

    def dashboard_page(*args, **kwargs):  # This decorator is required because the cog Dashboard may load after the third party when the bot is started.
        def decorator(func: typing.Callable):
            func.__dashboard_decorator_params__ = (args, kwargs)
            return func
        return decorator


    class DashboardIntegration:
        bot: Red

        @commands.Cog.listener()
        async def on_dashboard_cog_add(self, dashboard_cog: commands.Cog) -> None:  # `on_dashboard_cog_add` is triggered by the Dashboard cog automatically.
            try:
                from dashboard.rpc.thirdparties import dashboard_page
            except ImportError:  # Should never happen because the event would not be dispatched by the Dashboard cog, but...
                return
            for attr in dir(self):
                if hasattr((func := getattr(self, attr)), "__dashboard_decorator_params__"):  # Find all pages methods with the @dashboard_page decorator.
                    setattr(
                        self,
                        attr,
                        types.MethodType(
                            dashboard_page(
                                *func.__dashboard_decorator_params__[0],
                                **func.__dashboard_decorator_params__[1],
                            )(func.__func__),
                            func.__self__,
                        ),
                    )
            dashboard_cog.rpc.third_parties_handler.add_third_party(self)  # Add third party to the Dashboard.

        @dashboard_page(name=None)  # Create a default page for the third party (`name=None`). It will be available at the URL `/third_party/mycog`.
        async def rpc_callback(self, user: discord.User, **kwargs) -> dict:  # The kwarg `user` means that Red-Dashboard will request a connection from a bot user with OAuth from Discord.
            if user.id not in self.bot.owner_ids:
                return {"status": 1, "error_message": "You're not a bot owner!"}  # Return a error message who will be displayed by Red-Dashboard.
            return {"status": 0, "web-content": web_content, "title_content": "You're a bot owner!"}  # Return a web content with the text variable `title_content`.

        @dashboard_page(name="guild")  # Create a page nammed "guild" for the third party. It will be available at the URL `/third_party/mycog/guild`.
        async def rpc_callback(self, user: discord.User, guild: discord.Guild, **kwargs) -> dict:  # The kwarg `guild` means that Red-Dashboard will ask for the choice of a server among those to which the user has access.
            return {"status": 0, "web-content": web_content, "title_content": f"You're in guild {guild.name} ({guild.id})!"}  # Return a web content with the text variable `title_content`.

    web_content = """
    {% extends "base-site.html" %}

    {% block title %} {{ _('MyCog Cog') }} {% endblock title %}

    {% block content %}
    <h2>MyCog Cog</h2>
    <div class="row">
        <div class="col-md-12">
            <div class="card">
                <div class="card-body">
                    <h3>{{ title_content }}</h3>
                </div>
            </div>
        </div>
    </div>
    {% endblock content %}
    """

---------------------------------
Closing Words and Further Reading
---------------------------------

If you're reading this, it means that you've made it to the end of this guide.
Congratulations! You are now prepared with the Third Parties integration for Red-Dashboard.