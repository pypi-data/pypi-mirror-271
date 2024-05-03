# Core usage


???+ abstract "umami.track()"
    === "Examples"
        ```python
        import djade.core

        def my_function():
            djade.core.umami.track("someone went to my function!")
        
            data = djade.core.UmamiEventData(
                hostname="example.com",
                language = "en-GB",
                referrer = "",
                screen = "1920x1080",
                title = "abc",
                url = "/my_event",
                name = "My Custom Event"
            )
            
            djade.core.umami.track(data)
            
            djade.core.umami.track({
                "name": "My Custom Event",
                "url": "/my_page/123"
            })
        ```

??? abstract "umami.track_event_name()"
    === "Description"
        Track using just an event name
    === "Definition" 
        | PARAMETER  | DESCRIPTION  |  REQUIRED |
        |---|---|---|
        |  event_name _(string)_ |  The text of the event you'd like to send.  |  :fontawesome-solid-check: |

    === "Examples"
        ```python
        from djade.core import umami
        
        umami.track_event_name("My event")
        ```

??? abstract "umami.send()"
    === "Description"
        This is the manual method for sending a raw event
    === "Definitions"
        | PARAMETER | DESCRIPTION      | REQUIRED                  |
        |-----------|------------------|---------------------------|
        | payload  _([UmamiPayload](dataclasses.md#dataclass-umamipayload-source))_ |  | :fontawesome-solid-check: |
    === "Example"
        ```python
        from django-aws-config.core import umami
        
        umami.send({
            "website": "12345-6789...",
            "data": {
                "name": "my event"
            }
        })
        ```