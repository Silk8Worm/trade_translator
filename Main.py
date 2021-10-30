from Kivy.GUI import TradeTranslatorApp
import sentry_sdk
sentry_sdk.init(
    "https://eefd22745ff04bc4886ba664265be169@o350683.ingest.sentry.io/6024894",

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0
)


TradeTranslatorApp().run()


