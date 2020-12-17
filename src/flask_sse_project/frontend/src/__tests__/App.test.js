import React from 'react';
import { render, screen } from '@testing-library/react';
 
import Procedure from '../procedure';
 
describe('Init Seite', () => {
  test('0 Controller', () => {
    let data = {status: 'init', connectedController: 0};
    render(<Procedure data={data}/>);
    expect(screen.getByText(/There is no/)).toBeInTheDocument();
  });
  test('1 Controller', () => {
    let data = {status: 'init', connectedController: 1}
    render(<Procedure data={data}/>);
    expect(screen.getByText(/There is one/)).toBeInTheDocument();
  });
  test('2 Controller', () => {
    let data = {status: 'init', connectedController: 2}
    render(<Procedure data={data}/>);
    expect(screen.getByText(/There are two/)).toBeInTheDocument();
  });
});

describe('playerMenu Seite', () => {
  test('Render PlayerMenu', () => {
    let data = {status: 'playerMenu', fieldNames: ["1vs1", "2vs2"]}
    render(<Procedure data={data} />);
    expect(screen.getByText(/Choose the Playmode/))
  });
});

