import telegram
import config_provider
from file_handler.models import VmFilesCopyResult, FailReason


def get_telegram_bot() -> telegram.Bot:
    config = config_provider.get_config()
    return telegram.Bot(config.telegram_AT)


def convert_failed_reason_to_friendly(reason: FailReason) -> str:
    if reason == FailReason.DifferentSha256:
        return "hashes mismatch between origin and target"
    elif reason == FailReason.CopyFailed:
        return "error in copying files"
    else:
        return "unknown reason"


def prepare_message(results: [VmFilesCopyResult]) -> str:
    messages: [str] = []
    for res in results:
        if len(res.failed_copies) == 0:
            messages.append(f"*{res.vm.friendly_name}*\n Successfully copied all files")
            continue

        copied_files_str = ""
        for (origin, target) in copied_files_str:
            copied_files_str += f"{origin} to {target}\n"

        failed_files_str = ""
        for (failed_file, reason) in res.failed_copies:
            failed_files_str += f"File {failed_file} failed to" \
                                f" copy due to {convert_failed_reason_to_friendly(reason)}.\n"

        msg = f"""
*{res.vm.friendly_name}*
_Succeeded files_
```
{copied_files_str}
```

_Failed files:_
```
{failed_files_str}
```"""
        messages.append(msg)
    msg = ""
    for m in messages:
        msg += f"{m}\n"

    return msg


async def report(results: [VmFilesCopyResult]):
    bot = get_telegram_bot()
    async with bot:
        await bot.send_message(prepare_message(results))


async def report_error():
    pass
