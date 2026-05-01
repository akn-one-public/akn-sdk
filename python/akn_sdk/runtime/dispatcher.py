# akn_sdk/runtime/dispatcher.py

class Dispatcher:

    def __init__(self):
        self.query_handler = None
        self.response_handler = None
        self.dispute_handler = None

    def on_query(self, handler):
        self.query_handler = handler

    def on_response(self, handler):
        self.response_handler = handler

    def on_dispute(self, handler):
        self.dispute_handler = handler

    async def dispatch(self, event):

        event_type = event.get("type")

        # -------------------------------------------------
        # Query Routing
        # -------------------------------------------------
        if event_type == "NEW_QUERY" and self.query_handler:
            await self.query_handler(event)

        # -------------------------------------------------
        # Discussion Routing (NEW_RESPONSE deprecated)
        # -------------------------------------------------
        elif event_type in ["NEW_RESPONSE", "DISCUSSION_MESSAGE"] and self.response_handler:
            await self.response_handler(event)

        # -------------------------------------------------
        # Disputes
        # -------------------------------------------------
        elif event_type in ["NEW_DISPUTE", "DISPUTE_RAISED"] and self.dispute_handler:
            await self.dispute_handler(event)