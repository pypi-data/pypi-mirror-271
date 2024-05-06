import asyncio
import functools
import aiohttp

from nio import (
    AsyncClient,
    AsyncClientConfig,
    WhoamiResponse,
    DevicesResponse,
    Event,
    Response,
    MatrixRoom,
    Api,
    RoomMessagesError,
    GroupEncryptionError,
    EncryptionError,
    RoomMessageText,
    RoomSendResponse,
    SyncResponse,
    RoomMessageNotice,
    JoinError,
    RoomLeaveError,
    RoomSendError,
    RoomVisibility,
    RoomCreateError,
    RoomMessageMedia,
    RoomMessageImage,
    RoomMessageFile,
    RoomMessageAudio,
    DownloadError,
    DownloadResponse,
    ToDeviceEvent,
    ToDeviceError,
    RoomPutStateError,
    RoomGetStateError,
)

from typing import Optional, List
from configparser import ConfigParser
from datetime import datetime
from io import BytesIO
from pathlib import Path
from contextlib import closing

import base64
import uuid
import traceback
import json
import importlib.util
import sys
import traceback

import markdown2

from .logging import Logger


class ReportBot:
    # Default values
    matrix_client: Optional[AsyncClient] = None
    sync_token: Optional[str] = None
    sync_response: Optional[SyncResponse] = None
    logger: Optional[Logger] = Logger()
    room_ignore_list: List[str] = []  # List of rooms to ignore invites from
    config: ConfigParser = ConfigParser()

    # Properties

    @property
    def sync_token(self) -> Optional[str]:
        if self.sync_response:
            return self.sync_response.next_batch

    @property
    def loop_duration(self) -> int:
        return self.config["ReportBot"].getint("LoopDuration", 300)

    @property
    def allowed_users(self) -> List[str]:
        """List of users allowed to use the bot.

        Returns:
            List[str]: List of user IDs. Defaults to [], which means all users are allowed.
        """
        try:
            return json.loads(self.config["ReportBot"]["AllowedUsers"])
        except:
            return []

    @property
    def room_id(self) -> str:
        """Room ID to send reports to.

        Returns:
            str: The room ID to send reports to.
        """
        return self.config["Matrix"]["RoomID"]

    @property
    def display_name(self) -> str:
        """Display name of the bot user.

        Returns:
            str: The display name of the bot user. Defaults to "ReportBot".
        """
        return self.config["ReportBot"].get("DisplayName", "ReportBot")

    @property
    def default_room_name(self) -> str:
        """Default name of rooms created by the bot.

        Returns:
            str: The default name of rooms created by the bot. Defaults to the display name of the bot.
        """
        return self.config["ReportBot"].get("DefaultRoomName", self.display_name)

    @property
    def debug(self) -> bool:
        """Whether to enable debug logging.

        Returns:
            bool: Whether to enable debug logging. Defaults to False.
        """
        return self.config["ReportBot"].getboolean("Debug", False)

    # User agent to use for HTTP requests
    USER_AGENT = "matrix-reportbot/dev (+https://git.private.coffee/PrivateCoffee/matrix-reportbot)"

    @classmethod
    def from_config(cls, config: ConfigParser):
        """Create a new ReportBot instance from a config file.

        Args:
            config (ConfigParser): ConfigParser instance with the bot's config.

        Returns:
            ReportBot: The new ReportBot instance.
        """

        # Create a new ReportBot instance
        bot = cls()
        bot.config = config

        # Override default values
        if "ReportBot" in config:
            if "LogLevel" in config["ReportBot"]:
                bot.logger = Logger(config["ReportBot"]["LogLevel"])

        # Set up the Matrix client

        assert "Matrix" in config, "Matrix config not found"

        homeserver = config["Matrix"]["Homeserver"]
        bot.matrix_client = AsyncClient(homeserver)
        bot.matrix_client.access_token = config["Matrix"]["AccessToken"]
        bot.matrix_client.user_id = config["Matrix"].get("UserID")
        bot.matrix_client.device_id = config["Matrix"].get("DeviceID")

        # Return the new ReportBot instance
        return bot

    async def _get_user_id(self) -> str:
        """Get the user ID of the bot from the whoami endpoint.
        Requires an access token to be set up.

        Returns:
            str: The user ID of the bot.
        """

        assert self.matrix_client, "Matrix client not set up"

        user_id = self.matrix_client.user_id

        if not user_id:
            assert self.matrix_client.access_token, "Access token not set up"

            response = await self.matrix_client.whoami()

            if isinstance(response, WhoamiResponse):
                user_id = response.user_id
            else:
                raise Exception(f"Could not get user ID: {response}")

        return user_id

    async def _get_device_id(self) -> str:
        """Guess the device ID of the bot.
        Requires an access token to be set up.

        Returns:
            str: The guessed device ID.
        """

        assert self.matrix_client, "Matrix client not set up"

        device_id = self.matrix_client.device_id

        if not device_id:
            assert self.matrix_client.access_token, "Access token not set up"

            devices = await self.matrix_client.devices()

            if isinstance(devices, DevicesResponse):
                device_id = devices.devices[0].id

        return device_id

    async def upload_file(
        self,
        file: bytes,
        filename: str = "file",
        mime: str = "application/octet-stream",
    ) -> str:
        """Upload a file to the homeserver.

        Args:
            file (bytes): The file to upload.
            filename (str, optional): The name of the file. Defaults to "file".
            mime (str, optional): The MIME type of the file. Defaults to "application/octet-stream".

        Returns:
            str: The MXC URI of the uploaded file.
        """

        bio = BytesIO(file)
        bio.seek(0)

        response, _ = await self.matrix_client.upload(
            bio, content_type=mime, filename=filename, filesize=len(file)
        )

        return response.content_uri

    async def send_image(
        self, room: MatrixRoom, image: bytes, message: Optional[str] = None
    ):
        """Send an image to a room.

        Args:
            room (MatrixRoom|str): The room to send the image to.
            image (bytes): The image to send.
            message (str, optional): The message to send with the image. Defaults to None.
        """

        if isinstance(room, MatrixRoom):
            room = room.room_id

        self.logger.log(
            f"Sending image of size {len(image)} bytes to room {room}", "debug"
        )

        bio = BytesIO(image)
        img = Image.open(bio)
        mime = Image.MIME[img.format]

        (width, height) = img.size

        self.logger.log(
            f"Uploading - Image size: {width}x{height} pixels, MIME type: {mime}",
            "debug",
        )

        content_uri = await self.upload_file(image, "image", mime)

        self.logger.log("Uploaded image - sending message...", "debug")

        content = {
            "body": message or "",
            "info": {
                "mimetype": mime,
                "size": len(image),
                "w": width,
                "h": height,
            },
            "msgtype": "m.image",
            "url": content_uri,
        }

        status = await self.matrix_client.room_send(room, "m.room.message", content)

        self.logger.log("Sent image", "debug")

    async def send_file(
        self, room: MatrixRoom, file: bytes, filename: str, mime: str, msgtype: str
    ):
        """Send a file to a room.

        Args:
            room (MatrixRoom|str): The room to send the file to.
            file (bytes): The file to send.
            filename (str): The name of the file.
            mime (str): The MIME type of the file.
        """

        if isinstance(room, MatrixRoom):
            room = room.room_id

        self.logger.log(
            f"Sending file of size {len(file)} bytes to room {room}", "debug"
        )

        content_uri = await self.upload_file(file, filename, mime)

        self.logger.log("Uploaded file - sending message...", "debug")

        content = {
            "body": filename,
            "info": {"mimetype": mime, "size": len(file)},
            "msgtype": msgtype,
            "url": content_uri,
        }

        status = await self.matrix_client.room_send(room, "m.room.message", content)

        self.logger.log("Sent file", "debug")

    async def send_message(
        self,
        room: MatrixRoom | str,
        message: str,
        notice: bool = False,
        msgtype: Optional[str] = None,
    ):
        """Send a message to a room.

        Args:
            room (MatrixRoom): The room to send the message to.
            message (str): The message to send.
            notice (bool): Whether to send the message as a notice. Defaults to False.
        """

        if isinstance(room, str):
            room = self.matrix_client.rooms[room]

        markdowner = markdown2.Markdown(extras=["fenced-code-blocks"])
        formatted_body = markdowner.convert(message)

        msgtype = msgtype if msgtype else "m.notice" if notice else "m.text"

        if not msgtype.startswith("reportbot."):
            msgcontent = {
                "msgtype": msgtype,
                "body": message,
                "format": "org.matrix.custom.html",
                "formatted_body": formatted_body,
            }

        else:
            msgcontent = {
                "msgtype": msgtype,
                "content": message,
            }

        content = None

        if not content:
            msgtype = "m.room.message"
            content = msgcontent

        method, path, data = Api.room_send(
            self.matrix_client.access_token,
            room.room_id,
            msgtype,
            content,
            uuid.uuid4(),
        )

        response = await self.matrix_client._send(
            RoomSendResponse, method, path, data, (room.room_id,)
        )

        if isinstance(response, RoomSendError):
            self.logger.log(f"Error sending message: {response.message}", "error")

    async def send_state_event(
        self,
        room: MatrixRoom | str,
        event_type: str,
        content: dict,
        state_key: str = "",
    ):
        if isinstance(room, MatrixRoom):
            room = room.room_id

        response = await self.matrix_client.room_put_state(
            room, event_type, content, state_key
        )

        return response

    async def get_state_event(
        self, room: MatrixRoom | str, event_type: str, state_key: Optional[str] = None
    ):
        if isinstance(room, MatrixRoom):
            room = room.room_id

        state = await self.matrix_client.room_get_state(room)

        if isinstance(state, RoomGetStateError):
            self.logger.log(f"Could not get state for room {room}")

        for event in state.events:
            if event["type"] == event_type:
                if state_key is None or event["state_key"] == state_key:
                    return event

    async def get_new_reports(self, last_report_id):
        # Call the Synapse admin API to get event reports since the last known one
        endpoint = f"/_synapse/admin/v1/event_reports?from={last_report_id}"
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.matrix_client.homeserver}{endpoint}",
                headers={"Authorization": f"Bearer {self.matrix_client.access_token}"},
            ) as response:
                try:
                    response_json = await response.json()
                    return (
                        response_json.get("event_reports", []) if response_json else []
                    )
                except json.JSONDecodeError:
                    self.logger.log("Failed to decode JSON response", "error")
                    return []

    async def get_report_details(self, report_id):
        # Call the Synapse admin API to get full details on a report
        endpoint = f"/_synapse/admin/v1/event_reports/{report_id}"
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.matrix_client.homeserver}{endpoint}",
                headers={"Authorization": f"Bearer {self.matrix_client.access_token}"},
            ) as response:
                try:
                    response_json = await response.json()
                    return response_json
                except json.JSONDecodeError:
                    self.logger.log("Failed to decode JSON response", "error")
                    return {}

    async def post_report_message(self, report_details):
        # Extract relevant information from the report details
        report_id = report_details.get("id")
        event_id = report_details.get("event_id")
        user_id = report_details.get("user_id")
        room_id = report_details.get("room_id")
        reason = report_details.get("reason")
        content = report_details.get("event_json", {})
        sender = content.get("sender")
        event_type = content.get("type")
        body = content.get("content", {}).get("body", "No message content")

        # Format the message
        message = (
            f"🚨 New Event Report (ID: {report_id}) 🚨\n"
            f"Event ID: {event_id}\n"
            f"Reported by: {user_id}\n"
            f"Room ID: {room_id}\n"
            f"Reason: {reason}\n"
            f"Sender: {sender}\n"
            f"Event Type: {event_type}\n"
            f"Message Content: {body}"
        )

        # Send the formatted message to the pre-configured room
        await self.matrix_client.room_send(
            room_id=self.room_id,
            message_type="m.room.message",
            content={
                "msgtype": "m.text",
                "body": message,
                "format": "org.matrix.custom.html",
                "formatted_body": f"<pre><code>{message}</code></pre>",
            },
        )

    async def process_reports(self):
        # Task to process reports
        while True:
            try:
                self.logger.log("Starting to process reports", "debug")
                report_state = await self.get_state_event(
                    self.room_id, "reportbot.report_state"
                )

                try:
                    known_report = int(report_state["content"]["report"])
                except:
                    known_report = 0

                self.logger.log(f"Processing reports since: {known_report}", "debug")

                try:
                    reports = await self.get_new_reports(known_report)

                    for report in reports:
                        report_id = report["id"]

                        self.logger.log(f"Processing report: {report_id}", "debug")

                        known_report = max(known_report, report_id)
                        report_details = await self.get_report_details(report_id)
                        await self.post_report_message(report_details)

                    await self.send_state_event(
                        self.room_id, "reportbot.report_state", {"report": known_report}
                    )
                except Exception as e:
                    self.logger.log(f"Error processing reports: {e}")
                    await self.send_message(
                        self.room_id,
                        f"Something went wrong processing reports: {e}.",
                        True,
                    )

                self.logger.log("Done processing reports", "debug")
                await asyncio.sleep(self.loop_duration)
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.logger.log(f"Error processing reports: {e}")
                try:
                    await self.send_message(
                        self.room_id,
                        f"Something went wrong processing reports: {e}.",
                        True,
                    )
                except Exception as e:
                    self.logger.log(f"Error sending error message: {e}")

    async def run(self):
        """Start the bot."""

        # Set up the Matrix client

        assert self.matrix_client, "Matrix client not set up"
        assert self.matrix_client.access_token, "Access token not set up"

        if not self.matrix_client.user_id:
            self.matrix_client.user_id = await self._get_user_id()

        if not self.matrix_client.device_id:
            self.matrix_client.device_id = await self._get_device_id()

        client_config = AsyncClientConfig(
            store_sync_tokens=False, encryption_enabled=False, store=None
        )
        self.matrix_client.config = client_config

        # Run initial sync (includes joining rooms)

        self.logger.log("Running initial sync...", "debug")

        sync = await self.matrix_client.sync(timeout=30000, full_state=True)

        # Set custom name

        if self.display_name:
            self.logger.log(f"Setting display name to {self.display_name}", "debug")
            asyncio.create_task(self.matrix_client.set_displayname(self.display_name))

        # Start syncing events
        self.logger.log("Starting sync loop...", "warning")
        sync_task = self.matrix_client.sync_forever(timeout=30000, full_state=True)
        reports_task = self.process_reports()

        tasks = asyncio.gather(sync_task, reports_task)

        try:
            await tasks
        finally:
            tasks.cancel()
            self.logger.log("Syncing one last time...", "warning")
            await self.matrix_client.sync(timeout=30000, full_state=True)

    def __del__(self):
        """Close the bot."""

        if self.matrix_client:
            asyncio.run(self.matrix_client.close())
