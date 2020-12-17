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
    expect(screen.getByText(/Choose the Playmode/)).toBeInTheDocument();
  });
});

describe('nameMenu Seite', () => {
  test('Render nameMenu with error if playMode is null', () => {
    let data = {status: 'nameMenu', fieldNames: ["Orange", "Red", "Purple", "Blue", "Green", "Black"], playMode: null}
    render(<Procedure data={data} />);
    expect(screen.getByText(/Error NameMenu/)).toBeInTheDocument();
  });
  test('Render nameMenu with 2 tables for playMode = 1vs1', () => {
    let data = {status: 'nameMenu', fieldNames: ["Orange", "Red", "Purple", "Blue", "Green", "Black"], playMode: 1}
    render(<Procedure data={data} />);
    expect(screen.getAllByText(/Green/)).toHaveLength(2);
  });
  test('Render nameMenu with 4 tables for playMode = 2vs2', () => {
    let data = {status: 'nameMenu', fieldNames: ["Orange", "Red", "Purple", "Blue", "Green", "Black"], playMode: 2}
    render(<Procedure data={data} />);
    expect(screen.getAllByText(/Green/)).toHaveLength(4);
  });
});

describe('gameMenu Seite', () => {
  test('Render gameMenu', () => {
    let data = {status: 'gameMenu', fieldNames: ["Badminton", "Volleyball", "Tennis"]}
    render(<Procedure data={data} />);
    expect(screen.getByText(/Choose the Game/)).toBeInTheDocument();
  });
});

describe('changeSide Seite', () => {
  test('Render changeSide', () => {
    let data = {status: 'changeSide'}
    render(<Procedure data={data} />);
    expect(screen.getByText(/do you want to change Sides/)).toBeInTheDocument();
  });
});

describe('leaveGame Seite', () => {
  test('Render leaveGame', () => {
    let data = {status: 'leaveGame'}
    render(<Procedure data={data} />);
    expect(screen.getByText(/Do you want to leave the Game?/)).toBeInTheDocument();
  });
});





