# mautrix-twilio - A Matrix-Twilio relaybot bridge.
# Copyright (C) 2019 Tulir Asokan
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
from typing import Dict, Optional
import asyncio
import logging

from aiohttp import ClientSession, BasicAuth

from .data import TwilioUserID, TwilioAccountID, TwilioConversationID
from ..config import Config


class TwilioClient:
    log: logging.Logger = logging.getLogger("twilio.out")
    base_url: str = "https://api.twilio.com/2010-04-01"
    conversation_base_url: str = "https://conversations.twilio.com/v1/Conversations"
    http: ClientSession
    sender_id: TwilioUserID
    account_id: TwilioAccountID

    def __init__(self, config: Config, loop: asyncio.AbstractEventLoop) -> None:
        self.sender_id = config["twilio.sender_id"]
        self.account_id = config["twilio.account_id"]
        self.http = ClientSession(loop=loop, auth=BasicAuth(self.account_id,
                                                            config["twilio.secret"]))

    async def send_message(self, receiver: TwilioUserID, body: Optional[str] = None,
                           media: Optional[str] = None) -> Dict[str, str]:
        data = {
            "From": self.sender_id,
            "To": receiver,
        }
        if body:
            data["Body"] = body
        if media:
            data["MediaUrl"] = media
        self.log.debug(f"Sending message {data}")
        resp = await self.http.post(f"{self.base_url}/Accounts/{self.account_id}/Messages.json",
                                    data=data)
        return await resp.json()
    
    ## updates the 'friendly_name' of a given conversation (by ID) to match a matrix room address
    async def update_conversation_name(self, conversation_id: TwilioConversationID, room_address: str)
        data = {
            "FriendlyName": room_address
        }
    self.log.debug(f"Adding room address to conversation: {data}")
    resp = await self.http.post(f"{self.conversation_base_url}/{self.conversation_id}",
                                data=data)
    return await resp.json()

    ## also adds an identity to the conversation to send messages from using the Twilio number
    ## sets the identity to match the sending phone number, but should change later to mxid
    async def add_conversation_identity(self, conversation_id: TwilioConversationID):
        data = {
            "Identity": self.sender_id,
            "MessagingBinding.ProjectedAddress": self.sender_id
        }
    self.log.debug(f"Adding participant to conversation: {data}")
    resp = await self.http.post(f"{self.conversation_base_url}/{self.conversation_id}/Participants",
                                data=data)
    return await resp.json()

    async def send_conversation_message(self, conversation_id: TwilioConversationID, body: Optional[str] = None,
                                        media: Optional[str] = None) -> Dict[str, str]:
        data = {
            ## i'm 99% sure self.sender_id doesn't exist and should be replaced
            "Author": self.sender_id,
        }
        if body:
            data["Body"] = body
        if media:
            data["MediaUrl"] = media
        self.log.debug(f"Sending message {data}")
        resp = await self.http.post(f"{self.conversation_base_url}/{self.conversation_id}/Messages",
                                    data=data)
        return await resp.json()
