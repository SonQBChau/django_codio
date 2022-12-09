class DelayedGreeter extends Greeter {
  delay = 2000;
  constructor(name, delay) {
    super(name);
    if (delay !== undefined) {
      this.delay = delay;
    }
  }
  greet() {
    setTimeout(() => {
      this.showGreeting(this.getGreeting());
    }, this.delay);
  }
}
const dg2 = new DelayedGreeter("Patchy 2 Seconds");
dg2.greet();
const dg1 = new DelayedGreeter("Patchy 1 Second", 1000);
dg1.greet();
