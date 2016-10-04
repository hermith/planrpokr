import React from 'react';

const url = '/subscribe';

class TestComponent extends React.Component {

  componentWillMount() {
    this.state = { baboons: [], retries: 0, uuid: null };
    this.setUpEventSource();
  }

  setUpEventSource() {
    if (typeof EventSource === 'undefined') {
      this.addBaboon(
        <h2 key="fail">{"Your browser doesn't seem to support EventSource, please update and come back."}</h2>
      );
      return;
    }

    const source = new EventSource(url);

    source.addEventListener('open', (e) => {
      this.addBaboon(<h2 key={e.timeStamp}>Connection to server has been made</h2>);
    }, false);

    source.addEventListener('message', (e) => {
      const data = JSON.parse(e.data);

      if (data.uuid) {
        this.setUUID(data.uuid);
        this.addBaboon(<div key={e.timeStamp}>Your UUID is: {data.uuid}</div>);
      } else {
        this.addBaboon(<div key={e.timeStamp}>Message: {data}</div>);
      }
    }, false);

    source.addEventListener('error', (e) => {
      this.countRetry();
      if (this.state.retries >= 5) {
        source.close();
        this.addBaboon(<div key={e.timeStamp}>
          Connection to server has been closed.
          <button onClick={this.setUpEventSource()}>Retry</button>
        </div>);
      }
    }, false);
  }

  setUUID(uuid) {
    this.setState({ ...this.state, uuid });
  }

  countRetry() {
    this.setState({ ...this.state, retries: this.state.retries + 1 });
  }

  addBaboon(baboon) {
    this.state.baboons.push(baboon);
    const newState = { baboons: this.state.baboons };
    this.setState(newState);
  }

  render() {
    return (
      <div>
        <h1>Baboons:</h1>
        {this.state.baboons}
      </div>
    );
  }

}

export default TestComponent;
