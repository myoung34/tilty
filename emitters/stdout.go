
func (T StdOut) Emit() string {
	level.Info(Logger).Log("emitters.stdout", "test")
}
