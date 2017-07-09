export class QuestionBase<T>{
  value: T;
  key: string;
  label: string;
  required: boolean;
  controlType: string;
 
  constructor(options: {
      value?: T,
      key?: string,
      label?: string,
      required?: boolean,
      type?: string
    } = {}) {
    this.value = options.value;
    this.key = options.key || '';
    this.label = options.label || '';
    this.required = !!options.required;
    this.controlType = options.type || '';
  }
}
