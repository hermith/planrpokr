import React from 'react';
import ReactDOM from 'react-dom';
import TestComponent from './test/TestListenComponent';

const App = () => (
  <TestComponent />
);

ReactDOM.render(<App />, document.getElementById('app'));
