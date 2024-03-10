// react-component-wrapper.js
import React from 'react';
import ReactDOM from 'react-dom';
import SimpleReactComponent from './SimpleReactComponent';
import { Component } from '@angular/core';

@Component({
  selector: 'react-component-wrapper',
  template: '',
  standalone: true,
  styleUrls: [],
  inputs: ['message']
})
export class ReactComponentWrapper extends HTMLElement {
  connectedCallback() {
    this.render();
  }

  render() {
    ReactDOM.render(<SimpleReactComponent message="Hello from React" />, this);
  }
}

customElements.define('react-component-wrapper', ReactComponentWrapper);
