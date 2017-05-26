import { Pipe, PipeTransform } from '@angular/core';

@Pipe({name: 'keys'})
export class KeysPipe implements PipeTransform {
  transform(value, args:string[]) : any {
    let keys = [];
    for (let key in value) {
        let newWord = key.replace(/([a-z])([A-Z])/g, '$1 $2');
        newWord = newWord.charAt(0).toUpperCase() + newWord.slice(1);

        keys.push({key: newWord, val: value[key]});
    }
    return keys;
  }
}
