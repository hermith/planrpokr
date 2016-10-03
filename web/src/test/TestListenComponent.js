import React from 'react';

const url = '/subscribe';

class TestComponent extends React.Component {

  componentWillMount() {
    this.setUpEventSource();
  }

  setUpEventSource() {
    const source = new EventSource(url);

    source.addEventListener('open', (e) => {
      this.addBaboon(<h2 key={e.timeStamp}>Connection to server has been made</h2>);
    }, false);
    source.addEventListener('message', (e) => {
      this.addBaboon(<div key={e.timeStamp}>{e.data}</div>);
    }, false);
    source.addEventListener('error', (e) => {
      this.countRetry();
      if (this.state.retries >= 5) {
        source.close();
        this.addBaboon(<div key={e.timeStamp}>Connection to server has been closed.</div>);
      }
    }, false);

    this.state = { baboons: [], retries: 0 };
  }

  addBaboon(baboon) {
    this.state.baboons.push(baboon);
    const newState = { baboons: this.state.baboons };
    this.setState(newState);
  }

  countRetry() {
    this.setState({ ...this.state, retries: this.state.retries + 1 });
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
