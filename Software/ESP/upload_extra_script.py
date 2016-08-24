from SCons.Script import DefaultEnvironment
env = DefaultEnvironment()
env.Replace(
    NEWUPLOADER="esptool.py",
    NEWUPLOADERFLAGS=[
        "--port", "$UPLOAD_PORT",
        "--baud", "$UPLOAD_SPEED",
        "write_flash", "0x00000",
    ],
    UPLOADCMD='python $NEWUPLOADER $NEWUPLOADERFLAGS $SOURCE'
)
