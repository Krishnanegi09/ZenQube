# Platform-Specific Notes

## macOS Memory Limits

**Important**: macOS has limited support for memory limits via `RLIMIT_AS`.

### Behavior:
- ✅ **CPU limits**: Fully supported
- ⚠️ **Memory limits**: May show warning but continues execution
- ✅ **Process limits**: Not available (shows warning)
- ✅ **File size limits**: Fully supported

### Why?
macOS's implementation of `RLIMIT_AS` is different from Linux. The sandbox will:
- Log a warning if memory limit can't be set
- Continue execution (doesn't fail)
- Other limits (CPU, file size) still work

### For Full Memory Control:
- Use Linux for complete memory limit enforcement
- On macOS, CPU and file size limits are fully functional
- Memory monitoring still works via psutil in the web dashboard

## Windows

- Uses Job Objects for resource limits
- Limited support compared to Unix systems
- CPU and memory limits via Windows APIs

## Linux

- Full support for all resource limits
- All features work as expected

---

**Note**: The sandbox continues execution even if some limits can't be set, ensuring maximum compatibility across platforms.





