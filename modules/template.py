mb_mod = False  # Is this a module designed for use with Miror B.ot?
mb_import = False  # Should this module and its actions be automatically loaded by Miror B.ot?
mb_actions = {  # All actions must be named with a key.
    {
        "command": {  # "<Command key>": Command function, e.g. !echo = "echo": echo

        },
        "voice_join": {  # When a Member joins a voice channel

        },
        "voice_leave": {  # When a Member leaves a voice channel

        },
        "voice_update": {  # When a Member's voice state is updated

        },
        "voice_join_self": {  # When the bot joins a voice channel

        },
        "voice_leave_self": {  # When the bot leaves a voice channel

        },
        "guild_join": {  # When a new member joins the server

        },
        "guild_leave": {  # When a member leaves the server

        },
        "guild_update": {  # When a server is updated

        },
        "guild_available": {  # When a server becomes available to the bot

        },
        "guild_unavailable": {  # When a server becomes unavailable to the bot (usually due to Discord issues)

        },
        "guild_join_self": {  # When the bot joins a server

        },
        "guild_leave_self": {  # When the bot leaves a server

        },
        "connected": {  # When the bot successfully connects to Discord

        },
        "disconnected": {  # When the bot is disconnected from Discord (intended or otherwise)

        },
        "on_ready": {  # When the bot is ready to begin activities

        },
        "session_resumed": {  # When a suspended session is resumed

        },
        "error": {  # When an uncaught error occurs

        },
        "socket_receive": {  # When any data is received through the Discord WebSocket, pre-processing.

        },
        "socket_send": {  # When any data is sent through the Discord WebSocket, pre-processing.

        },
        "user_typing": {  # When a Member starts to type.

        },
        "on_message": {  # When a Discord message is received.

        },
        "on_message_self": {  # When the bot sends a Discord message.

        },
        "on_message_delete": {  # When an existing Discord message is deleted.

        },
        "on_bulk_message_delete": {  # When a bulk group of Discord messages are deleted.

        },
        "on_message_edit": {  # When a Discord message is edited.

        },
        "on_reaction_add": {  # When a reaction is added to a Discord message.

        },
        "on_reaction_remove": {  # When a reaction is removed from a Discord message.

        },
        "on_reaction_clear": {  # When all reactions are cleared from a Discord message.

        },
        "on_channel_create": {  # When a new Discord channel is created.

        },
        "on_channel_delete": {  # When an existing Discord channel is deleted.

        },
        "pins_update": {  # When the pins list of a Discord channel is updated.

        },
        "guild_integrations_update": {  # When a server's available integrations are updated.

        },
        "webhooks_update": {  # When a server's available webhooks are updated.

        },
        "member_update": {  # When a server Member is updated.

        },
        "user_update": {  # When a user's profile is updated.

        },
        "member_banned": {  # When an existing Member is banned from a server.

        },
        "member_unbanned": {  # When an existing Member is unbanned from a server.

        }
    }
}
