# -*- coding: utf-8 -*-

import random

from odoo import models, _


class MailBot(models.AbstractModel):
    _inherit = 'mail.bot'

    def _get_answer(self, record, body, values, command=False):
        # onboarding
        odoobot_state = self.env.user.odoobot_state
        if self._is_bot_in_private_channel(record):
            # main flow
            if odoobot_state == 'onboarding_emoji' and self._body_contains_emoji(body):
                self.env.user.odoobot_state = "onboarding_command"
                self.env.user.odoobot_failed = False
                return _(
                    "Great! 👍<br/>To access special commands, <b>start your sentence with</b> <span class=\"o_odoobot_command\">/</span>. Try getting help.")
            elif odoobot_state == 'onboarding_command' and command == 'help':
                self.env.user.odoobot_state = "onboarding_ping"
                self.env.user.odoobot_failed = False
                return _(
                    "Wow you are a natural!<br/>Ping someone with @username to grab their attention. <b>Try to ping me using</b> <span class=\"o_odoobot_command\">@InexoftBot</span> in a sentence.")
            elif odoobot_state == 'onboarding_ping' and self._is_bot_pinged(values):
                self.env.user.odoobot_state = "onboarding_attachement"
                self.env.user.odoobot_failed = False
                return _(
                    "Yep, I am here! 🎉 <br/>Now, try <b>sending an attachment</b>, like a picture of your cute dog...")
            elif odoobot_state == 'onboarding_attachement' and values.get("attachment_ids"):
                self.env.user.odoobot_state = "idle"
                self.env.user.odoobot_failed = False
                return _(
                    "I am a simple bot, but if that's a dog, he is the cutest 😊 <br/>Congratulations, you finished this tour. You can now <b>close this chat window</b>. Enjoy discovering Inexoft Software.")
            elif odoobot_state in (False, "idle", "not_initialized") and (_('start the tour') in body.lower()):
                self.env.user.odoobot_state = "onboarding_emoji"
                return _("To start, try to send me an emoji :)")
            # easter eggs
            elif odoobot_state == "idle" and body in ['❤️', _('i love you'), _('love')]:
                return _(
                    "Aaaaaw that's really cute but, you know, bots don't work that way. You're too human for me! Let's keep it professional ❤️")
            elif _('fuck') in body or "fuck" in body:
                return _("That's not nice! I'm a bot but I have feelings... 💔")
            # help message
            elif self._is_help_requested(body) or odoobot_state == 'idle':
                return _("Unfortunately, I'm just a bot 😞 I don't understand!")
            else:
                # repeat question
                if odoobot_state == 'onboarding_emoji':
                    self.env.user.odoobot_failed = True
                    return _(
                        "Not exactly. To continue the tour, send an emoji: <b>type</b> <span class=\"o_odoobot_command\">:)</span> and press enter.")
                elif odoobot_state == 'onboarding_attachement':
                    self.env.user.odoobot_failed = True
                    return _(
                        "To <b>send an attachment</b>, click on the <i class=\"fa fa-paperclip\" aria-hidden=\"true\"></i> icon and select a file.")
                elif odoobot_state == 'onboarding_command':
                    self.env.user.odoobot_failed = True
                    return _(
                        "Not sure what you are doing. Please, type <span class=\"o_odoobot_command\">/</span> and wait for the propositions. Select <span class=\"o_odoobot_command\">help</span> and press enter")
                elif odoobot_state == 'onboarding_ping':
                    self.env.user.odoobot_failed = True
                    return _(
                        "Sorry, I am not listening. To get someone's attention, <b>ping him</b>. Write <span class=\"o_odoobot_command\">@OdooBot</span> and select me.")
                return random.choice([
                    _("I'm not smart enough to answer your question.<br/>To follow my guide, ask: <span class=\"o_odoobot_command\">start the tour</span>."),
                    _("Hmmm..."),
                    _("I'm afraid I don't understand. Sorry!"),
                    _("Sorry I'm sleepy. Or not! Maybe I'm just trying to hide my unawareness of human language...<br/>I can show you features if you write: <span class=\"o_odoobot_command\">start the tour</span>.")
                ])
        return False
