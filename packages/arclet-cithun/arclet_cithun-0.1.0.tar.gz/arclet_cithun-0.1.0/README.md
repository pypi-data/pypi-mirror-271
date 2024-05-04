# Cithun

仿照 Linux 下的文件权限系统实现的权限管理系统。

WIP

## 特性

- 通过类似 Linux 下的文件权限系统的方式管理权限
- 支持用户组
- 支持用户组继承
- 可用上下文选择此时的权限

## Example

```python
from arclet.cithun import SyncMonitor, Node, NodeState, context, PermissionExecutor

monitor = SyncMonitor()

baz = Node("/foo/bar/baz").mkdir(parents=True)
qux = (baz / "qux").touch()

with context(scope="main"):
    admin = monitor.new_group('admin', 100)
    PermissionExecutor.root.set(admin, baz, NodeState("vma"))
    
    user = monitor.new_user('cithun')
    monitor.user_inherit(user, admin)
    
    assert PermissionExecutor.root.get(user, baz).most == NodeState("vma")
    assert not PermissionExecutor.root.get(user, qux).most.available
    
    PermissionExecutor.root.set(user, qux, NodeState(7))
    assert PermissionExecutor.root.get(user, qux).most.available

    PermissionExecutor.root.set(admin, baz, NodeState("v-a"))
    try:
        PermissionExecutor(user).set(user, qux, NodeState("vm-"))
    except PermissionError as e:
        print(e)  # Permission denied as /baz/ is not modifiable
```