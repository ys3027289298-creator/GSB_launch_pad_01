import json


def new_game():
    return {"items": {}, "load": 0, "capacity": 2, "stock": 100, "metric": 100, "day": 1, "id": 0, "fault": False, "resource": 10, "rate": 2, "clock": 0, "paused": False, "settled": False}


def save_state(state):
    return json.dumps(state, ensure_ascii=False)


def load_state(text):
    return json.loads(text)


def add(state, item_id, amount):
    if state.get("settled", False):
        return False
    if item_id in state["items"]:
        return False
    if amount <= 0 or amount > state["stock"]:
        return False
    state["items"][item_id] = amount
    state["stock"] -= amount
    return True


def receive(state, item_id):
    if state.get("settled", False):
        return False
    if state["load"] >= state["capacity"]:
        return False
    state["load"] += 1
    return True


def fee(state, item_id, end_day):
    return (end_day - state["day"]) * state["rate"]


def cancel(state, item_id):
    if state.get("settled", False):
        return False
    amount = state["items"].pop(item_id, None)
    if amount is None:
        return False
    state["stock"] += amount
    return True


def produce(state, amount):
    if state.get("settled", False) or state["fault"]:
        return False
    return True


def event(state):
    if state.get("settled", False):
        return state["metric"]
    state["metric"] -= 10
    return state["metric"]


def guard(state, item_id):
    return state["stock"] > 0 and state["resource"] > 0


def tick(state):
    if state.get("paused", False) or state.get("settled", False):
        return state["clock"]
    state["clock"] += 1
    return state["clock"]


def settle(state):
    state["settled"] = True
    return True


def main():
    print("命令: add/receive/fee/cancel/produce/event/guard/tick/settle/quit")
    state = new_game()
    while True:
        try:
            raw = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not raw:
            continue
        if raw == "quit":
            break
        parts = raw.split()
        cmd, args = parts[0], parts[1:]
        try:
            if cmd == "add":
                ok = add(state, int(args[0]), int(args[1]))
            elif cmd == "receive":
                ok = receive(state, int(args[0]))
            elif cmd == "fee":
                print(f"fee={fee(state, int(args[0]), int(args[1]))}")
                continue
            elif cmd == "cancel":
                ok = cancel(state, int(args[0]))
            elif cmd == "produce":
                ok = produce(state, int(args[0]))
            elif cmd == "event":
                print(f"metric={event(state)}")
                continue
            elif cmd == "guard":
                ok = guard(state, int(args[0]))
            elif cmd == "tick":
                print(f"clock={tick(state)}")
                continue
            elif cmd == "settle":
                ok = settle(state)
            else:
                print("error: unknown command")
                continue
        except (IndexError, ValueError):
            print("error: bad arguments")
            continue
        print("ok" if ok else "fail")


if __name__ == "__main__":
    main()
