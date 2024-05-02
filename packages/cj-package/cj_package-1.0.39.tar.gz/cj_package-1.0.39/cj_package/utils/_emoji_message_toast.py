import emoji

def _validate_message_type(func):
    def wrapper(message):
        if not isinstance(message, str):
            print(message)  # 如果message不是字符串类型，则直接输出message
            return None  # 返回None，不执行被装饰的函数
        else:
            return func(message)  # 如果message是字符串类型，则执行被装饰的函数
    return wrapper

@_validate_message_type
def success_toast(message: str):
    """
    输出成功消息，并添加成功的表情符号
    """
    success_emoji = emoji.emojize(':thumbs_up:' * 3, language='alias')
    print(f"{success_emoji} Success: {message}")

@_validate_message_type
def warning_toast(message: str):
    """
    输出警告消息，并添加警告的表情符号
    """
    warning_emoji = emoji.emojize(':warning:' * 3, language='alias')
    print(f"{warning_emoji} Warning: {message}")

@_validate_message_type
def failure_toast(message: str):
    """
    输出失败消息，并添加失败的表情符号
    """
    failure_emoji = emoji.emojize(':thumbs_down:' * 3, language='alias')
    print(f"{failure_emoji} Failure: {message}")


# 测试函数
if __name__ == "__main__":
    # 测试成功消息
    success_toast("Task completed successfully!")

    # 测试警告消息
    warning_toast("Low disk space detected.")

    # 测试失败消息
    failure_toast("Error: Connection timed out.")

    # 测试非字符串消息
    failure_toast(123)  # 直接输出数字 123，不执行函数