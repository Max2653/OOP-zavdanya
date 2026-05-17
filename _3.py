class Core:
    def boot(self):
        print("Core boot")


class PowerModule(Core):
    def boot(self):
        print("PowerModule boot")
        super().boot()


class SensorsModule(Core):
    def boot(self):
        print("SensorsModule boot")
        super().boot()


class CommsModule(Core):
    def boot(self):
        print("CommsModule boot")
        super().boot()


class LoggerModule(Core):
    def boot(self):
        print("LoggerModule boot")
        super().boot()


class SafetyModule(SensorsModule, LoggerModule):
    def boot(self):
        print("SafetyModule boot")
        super().boot()


class DiagnosticsModule(CommsModule, LoggerModule):
    def boot(self):
        print("DiagnosticsModule boot")
        super().boot()


class Robot(PowerModule, SafetyModule, DiagnosticsModule):
    pass


r = Robot()

print("=== BOOT ===")
r.boot()

print("\n=== MRO ===")
print(Robot.__mro__)


class LoggerModule(Core):
    def boot(self):
        print("LoggerModule boot")
        Core.boot(self)


class Robot(PowerModule, SafetyModule, DiagnosticsModule):
    pass


print("\n=== BOOT AFTER LoggerModule CHANGE ===")

r = Robot()
r.boot()


class Robot(SafetyModule, PowerModule, DiagnosticsModule):
    pass


print("\n=== NEW ROBOT ORDER ===")

r = Robot()
r.boot()

print("\n=== NEW MRO ===")
print(Robot.__mro__)