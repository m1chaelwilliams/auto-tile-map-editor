class StateManager:
    state: str = ""
    prev_state: str = ""
    @staticmethod
    def set_state(new_state: str):
        StateManager.prev_state = StateManager.state
        StateManager.state = new_state