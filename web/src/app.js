import React from 'react';
import ReactDOM from 'react-dom';
import TestComponent from './test/TestComponent';

const App = () => (
  <TestComponent />
);

ReactDOM.render(<App />, document.getElementById('app'));
