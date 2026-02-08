# JavaScript Interview Questions and Answers

# JavaScript Basics
## 1. What are primitive and non-primitive data types in JavaScript?

### **Primitive Data Types:**
Primitive data types are immutable and stored by value. They include:
- `String`
- `Number`
- `Boolean`
- `Undefined`
- `Null`
- `Symbol`
- `BigInt`

### **Non-Primitive Data Types:**
Non-primitive data types are mutable and stored by reference. They include:
- `Object`
- `Array`
- `Function`
---

## 2. What is the difference between `==` and `===`?

- `==` (Abstract Equality): Compares values **without** considering type conversion.
  ```js
  console.log(5 == '5'); // true (type coercion happens)
  ```
- `===` (Strict Equality): Compares values **with** type.
  ```js
  console.log(5 === '5'); // false (different types)
  ```

---

## 3. What is hoisting in JavaScript?

Hoisting is JavaScript's behavior of moving function and variable declarations to the top of their scope before execution.

Example:
```js
console.log(a); // undefined
var a = 10;
```

**Hoisted equivalent:**
```js
var a;
console.log(a); // undefined
a = 10;
```
**Note:** `let` and `const` are also hoisted but not initialized, causing a `ReferenceError` if accessed before declaration.

---

## 4. What is the difference between pass-by-value and pass-by-reference?

- **Pass-by-Value:** Changes inside the function do not affect the original variable (applies to primitive data types).
  ```js
  let x = 10;
  function modify(num) {
    num = 20;
  }
  modify(x);
  console.log(x); // 10 (unchanged)
  ```

- **Pass-by-Reference:** Changes inside the function affect the original variable (applies to objects and arrays).
  ```js
  let obj = { value: 10 };
  function modify(o) {
    o.value = 20;
  }
  modify(obj);
  console.log(obj.value); // 20 (changed)
  ```

---

## 5. How does JavaScript handle floating-point arithmetic errors? (`0.1 + 0.2 !== 0.3`)

JavaScript uses **IEEE 754 floating-point arithmetic**, which can cause precision errors.

Example:
```js
console.log(0.1 + 0.2); // 0.30000000000000004
console.log(0.1 + 0.2 === 0.3); // false
```

**Solution:** Use `toFixed()` or `Number.EPSILON` for precision.
```js
console.log((0.1 + 0.2).toFixed(2)); // '0.30'
console.log(Math.abs(0.1 + 0.2 - 0.3) < Number.EPSILON); // true
```

---

## 6. How do you check if a value is an array in JavaScript?

Use `Array.isArray(value)`:
```js
console.log(Array.isArray([1, 2, 3])); // true
console.log(Array.isArray({ key: 'value' })); // false
```

---

## 7. What is `typeof NaN` and why?

`typeof NaN` returns `'number'` because NaN is a special **invalid numeric value** in JavaScript.

Example:
```js
console.log(typeof NaN); // 'number'
console.log(NaN === NaN); // false (NaN is not equal to itself)
console.log(isNaN(NaN)); // true
```

---

## 8. What is the difference between `parseInt()` and `Number()`?

- `parseInt()`: Converts a string to an integer, stopping at non-numeric characters.
  ```js
  console.log(parseInt("42px")); // 42
  console.log(parseInt("3.14")); // 3
  ```
- `Number()`: Converts the entire string to a number, failing if non-numeric characters are present.
  ```js
  console.log(Number("42px")); // NaN
  console.log(Number("3.14")); // 3.14
  ```

---

## 9. How do you check if a variable is undefined or null?

Use `== null` (checks both `null` and `undefined`), or explicitly check both cases.

Example:
```js
let a;
console.log(a == null); // true (checks both undefined & null)
console.log(a === undefined); // true
console.log(a === null); // false
```

Alternative:
```js
if (typeof a === "undefined" || a === null) {
  console.log("Variable is either undefined or null");
}
```
# Functions and Scope in JavaScript

## What are first-class functions in JavaScript?
First-class functions are functions that can be assigned to variables, passed as arguments, and returned from other functions.

```javascript
const sayHello = function() { return "Hello"; };
const greet = sayHello;
console.log(greet()); // Output: Hello
```

## What is a pure function?
A pure function is a function that always returns the same output for the same input and has no side effects.

```javascript
function add(a, b) {
    return a + b;
}
console.log(add(2, 3)); // Output: 5
```

## Explain the difference between synchronous and asynchronous functions.
- **Synchronous** functions execute line by line and block the execution of further code.
- **Asynchronous** functions use callbacks, promises, or `async/await` to execute without blocking.

```javascript
console.log("Start");
setTimeout(() => console.log("Async Call"), 1000);
console.log("End");
// Output: Start, End, Async Call (after 1 second)
```

## How can you simulate function overloading in JavaScript?
JavaScript does not support function overloading directly, but it can be simulated using conditional statements or the `arguments` object.

```javascript
function multiply(a, b) {
    if (b === undefined) return a * a;
    return a * b;
}
console.log(multiply(2));    // Output: 4
console.log(multiply(2, 3)); // Output: 6
```

## What is the `call`, `apply`, and `bind` method in JavaScript?
- `call`: Invokes a function with a specified `this` value and arguments passed individually.
- `apply`: Similar to `call`, but arguments are passed as an array.
- `bind`: Returns a new function with a specified `this` value.

```javascript
function greet(name) {
    console.log(this.message + ' ' + name);
}
const obj = { message: "Hello" };
greet.call(obj, "John");  // Output: Hello John
greet.apply(obj, ["John"]); // Output: Hello John
const newGreet = greet.bind(obj);
newGreet("John");  // Output: Hello John
```

## How can you create a function that executes only once?
Using closures to store execution state.

```javascript
function once(fn) {
    let executed = false;
    return function(...args) {
        if (!executed) {
            executed = true;
            return fn(...args);
        }
    };
}
const init = once(() => console.log("Executed!"));
init(); // Output: Executed!
init(); // No output
```

## How do you implement memoization in JavaScript?
Memoization stores results of expensive function calls.

```javascript
function memoize(fn) {
    const cache = {};
    return function(...args) {
        const key = JSON.stringify(args);
        if (!cache[key]) cache[key] = fn(...args);
        return cache[key];
    };
}
const factorial = memoize(n => (n <= 1 ? 1 : n * factorial(n - 1)));
console.log(factorial(5)); // Output: 120
```

## Implement a currying function in JavaScript.
Currying transforms a function into a sequence of nested functions.

```javascript
function curry(fn) {
    return function curried(...args) {
        if (args.length >= fn.length) return fn(...args);
        return (...nextArgs) => curried(...args, ...nextArgs);
    };
}
const add = (a, b) => a + b;
const curriedAdd = curry(add);
console.log(curriedAdd(2)(3)); // Output: 5
```

## How do you implement a throttle function?
Throttling ensures a function is executed at most once in a given time period.

```javascript
function throttle(fn, limit) {
    let lastCall = 0;
    return function(...args) {
        const now = Date.now();
        if (now - lastCall >= limit) {
            lastCall = now;
            fn(...args);
        }
    };
}
```

## How do you implement a debounce function?
Debouncing delays function execution until a period of inactivity.

```javascript
function debounce(fn, delay) {
    let timer;
    return function(...args) {
        clearTimeout(timer);
        timer = setTimeout(() => fn(...args), delay);
    };
}
```

## Explain partial application in JavaScript.
Partial application fixes some arguments of a function and returns a new function.

```javascript
function partial(fn, ...fixedArgs) {
    return function(...remainingArgs) {
        return fn(...fixedArgs, ...remainingArgs);
    };
}
const add = (a, b, c) => a + b + c;
const add5 = partial(add, 5);
console.log(add5(10, 15)); // Output: 30
```

# JavaScript Objects, Prototypes, and Inheritance

## 1. What is the difference between `Object.freeze()`, `Object.seal()`, and `Object.preventExtensions()`?

### `Object.freeze()`
- Prevents adding, removing, or modifying properties.
- The object becomes completely immutable.
- Example:
  ```js
  const obj = { name: "John" };
  Object.freeze(obj);
  obj.name = "Doe"; // Does nothing
  obj.age = 30; // Does nothing
  delete obj.name; // Does nothing
  console.log(obj); // { name: "John" }
  ```

### `Object.seal()`
- Prevents adding or removing properties but allows modification of existing ones.
- Example:
  ```js
  const obj = { name: "John" };
  Object.seal(obj);
  obj.name = "Doe"; // Works
  obj.age = 30; // Does nothing
  delete obj.name; // Does nothing
  console.log(obj); // { name: "Doe" }
  ```

### `Object.preventExtensions()`
- Prevents adding new properties but allows modifying and deleting existing ones.
- Example:
  ```js
  const obj = { name: "John" };
  Object.preventExtensions(obj);
  obj.name = "Doe"; // Works
  obj.age = 30; // Does nothing
  delete obj.name; // Works
  console.log(obj); // {}
  ```

---

## 2. How does the prototype chain work in JavaScript?
- JavaScript uses a **prototype chain** to enable inheritance.
- Every object has an internal `[[Prototype]]` (accessible via `Object.getPrototypeOf(obj)` or `__proto__`).
- When accessing a property, JavaScript first looks at the object itself; if not found, it looks up the prototype chain.
- Example:
  ```js
  function Person(name) {
    this.name = name;
  }
  Person.prototype.sayHello = function() {
    return `Hello, my name is ${this.name}`;
  };
  const john = new Person("John");
  console.log(john.sayHello()); // "Hello, my name is John"
  console.log(john.__proto__ === Person.prototype); // true
  ```

---

## 3. What is the difference between `Object.assign()` and the spread operator?
### `Object.assign()`
- Copies properties from source objects into a target object.
- Performs **shallow copying**.
- Example:
  ```js
  const obj1 = { a: 1 };
  const obj2 = { b: 2 };
  const merged = Object.assign({}, obj1, obj2);
  console.log(merged); // { a: 1, b: 2 }
  ```

### Spread Operator (`...`)
- More concise syntax for copying properties.
- Also performs **shallow copying**.
- Example:
  ```js
  const obj1 = { a: 1 };
  const obj2 = { b: 2 };
  const merged = { ...obj1, ...obj2 };
  console.log(merged); // { a: 1, b: 2 }
  ```

---

## 4. What are ES6 classes, and how do they differ from constructor functions?
- ES6 classes provide a cleaner syntax for defining objects and inheritance.
- Under the hood, they use prototype-based inheritance like constructor functions.

### Constructor Function Example:
```js
function Person(name) {
  this.name = name;
}
Person.prototype.sayHello = function() {
  return `Hello, my name is ${this.name}`;
};
const john = new Person("John");
console.log(john.sayHello());
```

### ES6 Class Example:
```js
class Person {
  constructor(name) {
    this.name = name;
  }
  sayHello() {
    return `Hello, my name is ${this.name}`;
  }
}
const john = new Person("John");
console.log(john.sayHello());
```

---

## 5. How does the `super` keyword work in JavaScript?
- `super` calls a method from the parent class.
- Example:
```js
class Parent {
  constructor(name) {
    this.name = name;
  }
  greet() {
    return `Hello, I am ${this.name}`;
  }
}
class Child extends Parent {
  constructor(name, age) {
    super(name); // Calls Parent constructor
    this.age = age;
  }
}
const child = new Child("Alice", 25);
console.log(child.greet()); // "Hello, I am Alice"
```

---

## 6. Explain how method overriding works in JavaScript.
- A child class can override a method from the parent class.
- Example:
```js
class Parent {
  greet() {
    return "Hello from Parent";
  }
}
class Child extends Parent {
  greet() {
    return "Hello from Child";
  }
}
const obj = new Child();
console.log(obj.greet()); // "Hello from Child"
```

---

## **Complex Questions**

### 7. How do you **deep clone an object** in JavaScript?
```js
function deepClone(obj) {
  return JSON.parse(JSON.stringify(obj));
}
const obj = { a: { b: 1 } };
const cloned = deepClone(obj);
cloned.a.b = 2;
console.log(obj.a.b); // 1 (original object remains unchanged)
```

### 8. Implement **inheritance in JavaScript** without using `class`.
```js
function Parent(name) {
  this.name = name;
}
Parent.prototype.greet = function() {
  return `Hello, I am ${this.name}`;
};
function Child(name, age) {
  Parent.call(this, name); // Call Parent constructor
  this.age = age;
}
Child.prototype = Object.create(Parent.prototype);
Child.prototype.constructor = Child;
const child = new Child("Alice", 25);
console.log(child.greet()); // "Hello, I am Alice"
```

### 9. How do you **polyfill Object.create()**?
```js
function create(proto) {
  function F() {}
  F.prototype = proto;
  return new F();
}
const obj = { a: 1 };
const newObj = create(obj);
console.log(newObj.a); // 1
```
# ES6+ Features

## What are template literals, and why are they useful?
Template literals are a way to create strings in JavaScript using backticks (`` ` ``) instead of quotes. They allow for multi-line strings and string interpolation using `${}`.

### Example:
```js
const name = "John";
console.log(`Hello, ${name}!`); // Output: Hello, John!
```

They are useful because they improve readability and make string concatenation easier.

---

## What is destructuring, and how is it used?
Destructuring is a feature that allows extracting values from arrays or properties from objects into distinct variables.

### Array Destructuring:
```js
const numbers = [1, 2, 3];
const [first, second] = numbers;
console.log(first, second); // Output: 1 2
```

### Object Destructuring:
```js
const person = { name: "Alice", age: 25 };
const { name, age } = person;
console.log(name, age); // Output: Alice 25
```

---

## Explain the difference between `map()`, `filter()`, and `reduce()`
- `map()`: Transforms each array element and returns a new array.
- `filter()`: Filters elements based on a condition and returns a new array.
- `reduce()`: Reduces an array to a single value based on an accumulator function.

### Example:
```js
const numbers = [1, 2, 3, 4, 5];
const squared = numbers.map(num => num * num);
console.log(squared); // [1, 4, 9, 16, 25]

const evens = numbers.filter(num => num % 2 === 0);
console.log(evens); // [2, 4]

const sum = numbers.reduce((acc, num) => acc + num, 0);
console.log(sum); // 15
```

---

## What are generators, and how do they work?
Generators are special functions that can pause execution and resume later using the `yield` keyword.

### Example:
```js
function* generatorFunction() {
    yield 1;
    yield 2;
    yield 3;
}
const gen = generatorFunction();
console.log(gen.next().value); // 1
console.log(gen.next().value); // 2
console.log(gen.next().value); // 3
```

They are useful for handling asynchronous operations and iterating over sequences.

---

## What is the purpose of the `Symbol` type in JavaScript?
Symbols are unique and immutable values primarily used as object property keys to prevent naming conflicts.

### Example:
```js
const uniqueKey = Symbol("description");
const obj = { [uniqueKey]: "value" };
console.log(obj[uniqueKey]); // Output: value
```

They help create private object properties and avoid accidental overrides.

---

## Explain how `WeakMap` and `WeakSet` work
- `WeakMap`: A map where keys must be objects, and references to keys are weak.
- `WeakSet`: A set where values must be objects, and references are weak.

### Example:
```js
let obj = { key: "value" };
const weakMap = new WeakMap();
weakMap.set(obj, "some data");
console.log(weakMap.get(obj)); // Output: some data

const weakSet = new WeakSet();
weakSet.add(obj);
console.log(weakSet.has(obj)); // Output: true
```

They are useful for storing metadata or caches without preventing garbage collection.

---

## How would you implement a custom iterator in JavaScript?
A custom iterator can be implemented using the `[Symbol.iterator]` method.

### Example:
```js
const customIterable = {
    values: [10, 20, 30],
    [Symbol.iterator]() {
        let index = 0;
        return {
            next: () => {
                return index < this.values.length
                    ? { value: this.values[index++], done: false }
                    : { done: true };
            }
        };
    }
};

for (const value of customIterable) {
    console.log(value); // Output: 10, 20, 30
}
```

---

## How do ES6 Proxies work, and what are some real-world use cases?
Proxies allow custom behavior for fundamental operations like property access, assignment, and function calls.

### Example:
```js
const handler = {
    get(target, property) {
        return property in target ? target[property] : "Property not found";
    },
    set(target, property, value) {
        console.log(`Setting ${property} to ${value}`);
        target[property] = value;
    }
};

const obj = new Proxy({}, handler);
obj.name = "John";
console.log(obj.name); // Output: John
console.log(obj.age); // Output: Property not found
```

### Real-world use cases:
- **Data validation** before setting object properties.
- **Logging and debugging** for tracking object modifications.
- **Auto-filling default values** in objects.

# Asynchronous JavaScript Interview Questions and Answers

## 1. What is the event loop in JavaScript?
The event loop is a mechanism in JavaScript that handles asynchronous operations. It continuously checks the call stack and task queue, ensuring that the JavaScript runtime remains non-blocking by executing tasks when the call stack is empty.

### How it works:
1. JavaScript executes code in a single-threaded manner.
2. Asynchronous operations (e.g., setTimeout, Promises, event listeners) are handled by the browser or Node.js runtime.
3. Once the call stack is empty, the event loop moves tasks from the task queue (or microtask queue) into the call stack for execution.

---

## 2. How does the JavaScript call stack work?
The call stack is a data structure used to keep track of function calls in JavaScript. It follows the **LIFO (Last In, First Out)** principle.

### Example:
```js
function first() {
  second();
}

function second() {
  console.log("Hello, World!");
}

first();
```
**Execution Process:**
1. `first()` is pushed onto the call stack.
2. `first()` calls `second()`, which is pushed onto the call stack.
3. `console.log()` executes and is popped off the stack.
4. `second()` finishes execution and is removed from the stack.
5. `first()` finishes execution and is removed from the stack.

---

## 3. What is the difference between a macro-task and a micro-task?
- **Macro-task**: Scheduled in the task queue and executed after the call stack is empty. (e.g., `setTimeout`, `setInterval`, `setImmediate` in Node.js, I/O operations)
- **Micro-task**: Higher priority and executed immediately after the current execution context is cleared. (e.g., Promises, `process.nextTick` in Node.js)

### Execution Order Example:
```js
console.log("Start");

setTimeout(() => console.log("Macro-task: setTimeout"), 0);

Promise.resolve().then(() => console.log("Micro-task: Promise"));

console.log("End");
```
**Output:**
```
Start
End
Micro-task: Promise
Macro-task: setTimeout
```

---

## 4. What is the difference between `Promise.all()`, `Promise.race()`, and `Promise.any()`?
### `Promise.all()`
Waits for all promises to resolve, or rejects if any fails.
```js
Promise.all([
  Promise.resolve(1),
  Promise.resolve(2),
  Promise.reject("Error")
]).catch(console.error); // Output: "Error"
```

### `Promise.race()`
Resolves or rejects as soon as one promise settles.
```js
Promise.race([
  new Promise(res => setTimeout(() => res("Fast"), 100)),
  new Promise(res => setTimeout(() => res("Slow"), 500))
]).then(console.log); // Output: "Fast"
```

### `Promise.any()`
Resolves as soon as the first successful promise settles.
```js
Promise.any([
  Promise.reject("Error"),
  Promise.resolve("Success"),
  Promise.resolve("Another Success")
]).then(console.log); // Output: "Success"
```

---

## 5. What is `async` and `await`? How does it differ from `.then()`?
`async` and `await` simplify promise handling by allowing asynchronous code to be written in a synchronous style.

### Example using `.then()`:
```js
fetch("https://jsonplaceholder.typicode.com/todos/1")
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error(error));
```

### Example using `async`/`await`:
```js
async function fetchData() {
  try {
    let response = await fetch("https://jsonplaceholder.typicode.com/todos/1");
    let data = await response.json();
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}
fetchData();
```

**Key Differences:**
- `async/await` makes code more readable.
- It uses try/catch for error handling instead of `.catch()`.

---

## 6. How does `fetch()` work in JavaScript?
`fetch()` is used to make HTTP requests and returns a promise.

### Example:
```js
fetch("https://jsonplaceholder.typicode.com/posts")
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error("Fetch error:", error));
```

---

## 7. Explain the difference between `process.nextTick()` and `setImmediate()` in Node.js.
- `process.nextTick()`: Executes a callback **before** moving to the next event loop phase.
- `setImmediate()`: Executes a callback **in the next event loop cycle**.

### Example:
```js
console.log("Start");

process.nextTick(() => console.log("process.nextTick"));
setImmediate(() => console.log("setImmediate"));

console.log("End");
```
**Output:**
```
Start
End
process.nextTick
setImmediate
```

---

# Complex Questions

## 8. How would you implement a custom Promise class from scratch?
```js
class MyPromise {
  constructor(executor) {
    this.callbacks = [];
    this.state = "PENDING";
    this.value = null;

    const resolve = (value) => {
      if (this.state === "PENDING") {
        this.state = "FULFILLED";
        this.value = value;
        this.callbacks.forEach(cb => cb(value));
      }
    };

    executor(resolve);
  }

  then(callback) {
    if (this.state === "FULFILLED") {
      callback(this.value);
    } else {
      this.callbacks.push(callback);
    }
  }
}
```

---

## 9. How does Web Workers work in JavaScript?
Web Workers allow JavaScript to run in the background without blocking the main thread.

### Example:
**worker.js**
```js
self.onmessage = function(e) {
  self.postMessage(`Message received: ${e.data}`);
};
```
**main.js**
```js
const worker = new Worker("worker.js");
worker.postMessage("Hello, Worker!");
worker.onmessage = function(e) {
  console.log(e.data);
};
```

---

## 10. Implement an async queue that limits concurrent async operations.
```js
class AsyncQueue {
  constructor(limit) {
    this.queue = [];
    this.limit = limit;
    this.activeCount = 0;
  }

  enqueue(task) {
    return new Promise((resolve) => {
      this.queue.push(() => task().then(resolve));
      this.runNext();
    });
  }

  runNext() {
    if (this.activeCount < this.limit && this.queue.length) {
      this.activeCount++;
      const nextTask = this.queue.shift();
      nextTask().finally(() => {
        this.activeCount--;
        this.runNext();
      });
    }
  }
}
```

This queue ensures only `limit` number of tasks run concurrently.

---
# JavaScript DOM and Events Interview Questions

## 1. What are different ways to select an element in JavaScript?
JavaScript provides multiple ways to select DOM elements:
- `document.getElementById('id')` – Selects an element by its ID.
- `document.getElementsByClassName('class')` – Returns a live HTMLCollection of elements with the specified class name.
- `document.getElementsByTagName('tag')` – Returns a live HTMLCollection of elements with the specified tag.
- `document.querySelector('selector')` – Returns the first element that matches the CSS selector.
- `document.querySelectorAll('selector')` – Returns a static NodeList of all elements that match the selector.

## 2. Explain event delegation with an example.
Event delegation is a pattern where a parent element listens for events on its children instead of attaching listeners to individual child elements.

**Example:**
```js
// Instead of adding event listeners to each button, add one to the parent
const parent = document.getElementById('parent');
parent.addEventListener('click', function(event) {
    if (event.target && event.target.matches('button')) {
        console.log('Button clicked:', event.target.innerText);
    }
});
```

## 3. What is the difference between `stopPropagation()` and `preventDefault()`?
- `stopPropagation()` stops the event from propagating to parent elements.
- `preventDefault()` prevents the default behavior of an event (e.g., stopping a form submission or a link navigation).

**Example:**
```js
document.getElementById('link').addEventListener('click', function(event) {
    event.preventDefault(); // Stops navigation
    console.log('Link clicked, but navigation prevented');
});
```

## 4. What is the difference between `localStorage`, `sessionStorage`, and `cookies`?
| Feature         | localStorage | sessionStorage | cookies |
|----------------|-------------|---------------|---------|
| Data Storage  | Stores data with no expiration | Stores data for the session | Stores data with expiration |
| Accessibility | Only in the same origin | Only in the same session | Sent with every HTTP request |
| Storage Limit | 5-10 MB | 5-10 MB | 4 KB |

## 5. How does `MutationObserver` work in JavaScript?
`MutationObserver` allows you to watch for changes in the DOM.

**Example:**
```js
const observer = new MutationObserver(mutations => {
    mutations.forEach(mutation => {
        console.log('Mutation detected:', mutation);
    });
});

observer.observe(document.getElementById('target'), { childList: true, subtree: true });
```

## 6. How do you implement infinite scrolling in JavaScript?
Infinite scrolling loads new content as the user scrolls down.

**Example:**
```js
window.addEventListener('scroll', function() {
    if (window.innerHeight + window.scrollY >= document.body.offsetHeight) {
        loadMoreContent();
    }
});

function loadMoreContent() {
    console.log('Loading more content...');
    // Fetch new data and append it to the DOM
}
```

## Complex Questions

### 1. Implement a Virtual DOM from scratch.
```js
class VNode {
    constructor(tag, props, children) {
        this.tag = tag;
        this.props = props;
        this.children = children;
    }
}

function render(vnode) {
    if (typeof vnode === 'string') return document.createTextNode(vnode);
    const element = document.createElement(vnode.tag);
    for (let prop in vnode.props) {
        element.setAttribute(prop, vnode.props[prop]);
    }
    vnode.children.forEach(child => {
        element.appendChild(render(child));
    });
    return element;
}

const vdom = new VNode('div', { class: 'container' }, [
    new VNode('h1', {}, ['Virtual DOM Example']),
    new VNode('p', {}, ['This is a simple virtual DOM implementation.'])
]);

document.body.appendChild(render(vdom));
```

### 2. Implement a Drag-and-Drop Feature using Vanilla JavaScript
```js
const item = document.getElementById('draggable');
item.addEventListener('dragstart', (e) => {
    e.dataTransfer.setData('text/plain', e.target.id);
});

document.getElementById('dropzone').addEventListener('dragover', (e) => {
    e.preventDefault();
});

document.getElementById('dropzone').addEventListener('drop', (e) => {
    e.preventDefault();
    const data = e.dataTransfer.getData('text');
    e.target.appendChild(document.getElementById(data));
});
```

### 3. How do you create a custom event listener in JavaScript?
```js
class EventEmitter {
    constructor() {
        this.events = {};
    }

    on(event, listener) {
        if (!this.events[event]) {
            this.events[event] = [];
        }
        this.events[event].push(listener);
    }

    emit(event, ...args) {
        if (this.events[event]) {
            this.events[event].forEach(listener => listener(...args));
        }
    }
}

const emitter = new EventEmitter();
emitter.on('hello', name => console.log(`Hello, ${name}!`));
emitter.emit('hello', 'John');
```
# Error Handling & Debugging in JavaScript

## 1. What is the difference between `throw` and `try...catch`?
The `throw` statement is used to raise custom errors, whereas `try...catch` is used to handle exceptions gracefully.

### Example:
```javascript
function divide(a, b) {
    if (b === 0) {
        throw new Error("Cannot divide by zero");
    }
    return a / b;
}

try {
    console.log(divide(10, 0));
} catch (error) {
    console.error("Error caught:", error.message);
}
```

## 2. How do you handle errors in async functions?
Errors in async functions can be handled using `try...catch` inside an `async` function or by attaching a `.catch()` method to a promise.

### Example:
```javascript
async function fetchData() {
    try {
        let response = await fetch('https://api.example.com/data');
        let data = await response.json();
        console.log(data);
    } catch (error) {
        console.error("Error fetching data:", error);
    }
}
fetchData();
```

Using `.catch()`:
```javascript
fetch('https://api.example.com/data')
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error("Error fetching data:", error));
```

## 3. What is the purpose of the `finally` block in a try-catch statement?
The `finally` block is executed regardless of whether an error occurs or not. It is often used for cleanup operations.

### Example:
```javascript
function processFile() {
    try {
        console.log("Processing file...");
        throw new Error("File not found");
    } catch (error) {
        console.error("Error:", error.message);
    } finally {
        console.log("Closing file");
    }
}
processFile();
```

## 4. What is the difference between `window.onerror` and `try...catch`?
- `try...catch` only catches errors inside its block.
- `window.onerror` acts as a global error handler for unhandled errors in the browser.

### Example:
```javascript
window.onerror = function(message, source, lineno, colno, error) {
    console.error("Global Error Handler:", message, "at", source, "Line:", lineno);
};

throw new Error("Unexpected error occurred");
```

# Complex Questions

## 5. How would you implement a **custom global error handler** for an application?
A custom global error handler can be implemented using `window.onerror` for client-side applications or `process.on('uncaughtException')` for Node.js.

### Example (Client-Side):
```javascript
window.onerror = function(message, source, lineno, colno, error) {
    console.error("Global Error:", message, "at", source, "Line:", lineno);
    // Log the error to a monitoring service
};
```

### Example (Node.js):
```javascript
process.on('uncaughtException', (error) => {
    console.error("Uncaught Exception:", error.message);
    process.exit(1);
});
```

## 6. How do you handle **errors in event listeners**?
Errors in event listeners should be wrapped in a try-catch block to prevent the error from stopping other event handlers.

### Example:
```javascript
document.getElementById("btn").addEventListener("click", function() {
    try {
        throw new Error("Button click failed");
    } catch (error) {
        console.error("Error in event listener:", error.message);
    }
});
```

Alternatively, use a centralized error-handling function:
```javascript
function safeEventListener(callback) {
    return function(event) {
        try {
            callback(event);
        } catch (error) {
            console.error("Error in event listener:", error);
        }
    };
}

document.getElementById("btn").addEventListener("click", safeEventListener(() => {
    throw new Error("Something went wrong!");
}));
```
# JavaScript Performance Optimization

## What are memory leaks in JavaScript, and how can they be prevented?
### Memory Leaks:
Memory leaks occur when allocated memory is not properly released, leading to excessive memory consumption and degraded performance.

### Common Causes of Memory Leaks:
1. **Global Variables** - Variables declared without `let`, `const`, or `var` remain in memory.
2. **Closures Holding References** - Functions that hold references to outer variables prevent garbage collection.
3. **DOM References** - Detached DOM elements that are still referenced in JavaScript.
4. **Timers & Intervals** - `setTimeout` or `setInterval` not cleared when no longer needed.
5. **Event Listeners** - Unremoved event listeners on detached elements.

### Prevention Methods:
- Use `let` and `const` instead of `var` to prevent accidental global variables.
- Remove event listeners using `removeEventListener()` when elements are no longer needed.
- Clear intervals and timeouts using `clearInterval()` and `clearTimeout()`.
- Nullify DOM references after removing elements.

---
## What is the difference between `setTimeout(fn, 0)` and `requestAnimationFrame()`?

### `setTimeout(fn, 0)`:
- Executes the function after at least 0 milliseconds (next event loop cycle).
- Uses the **Event Loop** and places tasks in the **callback queue**.
- Not optimized for rendering.

### `requestAnimationFrame(fn)`:
- Optimized for animations; calls the function before the next repaint.
- Uses the **browser's rendering engine**.
- More efficient for animations than `setTimeout` or `setInterval`.

Use **`requestAnimationFrame()`** for smooth animations, and **`setTimeout(fn, 0)`** for deferring execution.

---
## What is tail call optimization in JavaScript?

### Tail Call Optimization (TCO):
- An optimization technique where the last function call in a recursive function does not increase the call stack.
- JavaScript engines (like V8) optimize certain recursive calls to prevent stack overflow.

### Example:
```javascript
function factorial(n, acc = 1) {
    if (n === 1) return acc;
    return factorial(n - 1, n * acc);
}
console.log(factorial(5)); // 120
```
- Here, `factorial(n - 1, n * acc)` is in **tail position**, meaning no extra stack frame is used.

**Note:** Tail Call Optimization is available in strict mode (`"use strict"`) in some JavaScript engines.

---
## How does JavaScript handle garbage collection?

### JavaScript Garbage Collection Mechanism:
- JavaScript uses **automatic garbage collection** with a mechanism called **Mark-and-Sweep**.
- When objects are no longer accessible, they are marked as garbage and removed.

### Garbage Collection Process:
1. **Mark Phase**: Identify objects still in use.
2. **Sweep Phase**: Remove unreferenced objects.

### Example:
```javascript
let obj = { key: 'value' };
obj = null; // Eligible for garbage collection
```

### Optimizations:
- Use **WeakMap** and **WeakSet** for objects that can be garbage-collected when no longer referenced.
- Avoid circular references (objects referencing each other).

---
## What is the difference between `Linked List` and `Array` performance-wise in JavaScript?

| Feature        | Linked List | Array |
|---------------|------------|-------|
| Access Time   | O(n)       | O(1) (indexed access) |
| Insertion/Deletion | O(1) (at beginning) | O(n) (shifting elements required) |
| Memory Usage  | More (extra pointers) | Less |

### Use Cases:
- **Arrays**: Fast random access (e.g., when using `arr[i]`).
- **Linked Lists**: Fast insertions/deletions (e.g., in a queue or stack implementation).

---
## Implement a Lazy-Loading Image Feature in JavaScript

### Using Intersection Observer API:
```javascript
document.addEventListener("DOMContentLoaded", function() {
    let lazyImages = document.querySelectorAll("img[data-src]");
    let observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                let img = entry.target;
                img.src = img.getAttribute("data-src");
                img.removeAttribute("data-src");
                observer.unobserve(img);
            }
        });
    });
    lazyImages.forEach(img => observer.observe(img));
});
```
### Usage in HTML:
```html
<img data-src="image.jpg" alt="Lazy Image" />
```
---
## How would you optimize a large JSON dataset for rendering in the browser?

### Optimization Techniques:
1. **Pagination** - Load a subset of data at a time.
2. **Virtualization** - Render only visible items (e.g., using React Virtual DOM).
3. **Compression** - Minify JSON before transferring.
4. **IndexedDB/LocalStorage** - Store processed JSON data locally.

### Example: Paginating a Large JSON Array
```javascript
function paginateData(data, pageSize, page) {
    return data.slice((page - 1) * pageSize, page * pageSize);
}
```

---
## Implement Infinite Scrolling using Intersection Observer API

### JavaScript Code:
```javascript
document.addEventListener("DOMContentLoaded", function() {
    let observer = new IntersectionObserver((entries) => {
        let lastEntry = entries[0];
        if (lastEntry.isIntersecting) {
            loadMoreItems();
        }
    });
    
    let sentinel = document.getElementById("sentinel");
    observer.observe(sentinel);
});

function loadMoreItems() {
    let list = document.getElementById("item-list");
    for (let i = 0; i < 10; i++) {
        let item = document.createElement("div");
        item.className = "item";
        item.textContent = `Item ${list.children.length + 1}`;
        list.appendChild(item);
    }
}
```

### Usage in HTML:
```html
<div id="item-list"></div>
<div id="sentinel"></div>
```

---
**End of Document**
# JavaScript Design Patterns

## 1. Module Pattern
The Module Pattern is a design pattern used to create encapsulated modules with private and public properties.
It helps in organizing code and preventing global scope pollution.

### Example:
```javascript
const Module = (function() {
    let privateVar = "I am private";

    function privateMethod() {
        console.log("Accessing private method");
    }

    return {
        publicMethod: function() {
            console.log("Accessing public method");
            privateMethod();
        }
    };
})();

Module.publicMethod(); // Works
// Module.privateMethod(); // Error: privateMethod is not defined
```

## 2. Singleton Pattern
The Singleton Pattern ensures that a class has only one instance and provides a global point of access to it.

### Example:
```javascript
const Singleton = (function() {
    let instance;

    function createInstance() {
        return { message: "I am the singleton instance" };
    }

    return {
        getInstance: function() {
            if (!instance) {
                instance = createInstance();
            }
            return instance;
        }
    };
})();

const instance1 = Singleton.getInstance();
const instance2 = Singleton.getInstance();

console.log(instance1 === instance2); // true
```

## 3. Observer Pattern
The Observer Pattern is used to create a one-to-many dependency between objects. When one object changes state, all its dependents are notified automatically.

### Example:
```javascript
class Observer {
    constructor() {
        this.subscribers = [];
    }
    subscribe(fn) {
        this.subscribers.push(fn);
    }
    unsubscribe(fn) {
        this.subscribers = this.subscribers.filter(sub => sub !== fn);
    }
    notify(data) {
        this.subscribers.forEach(sub => sub(data));
    }
}

const observer = new Observer();

const logData = data => console.log("Received:", data);
observer.subscribe(logData);
observer.notify("Hello Observers!"); // Outputs: Received: Hello Observers!
observer.unsubscribe(logData);
```

## 4. Factory Pattern
The Factory Pattern is used to create objects without exposing the creation logic to the client and refers to a common interface.

### Example:
```javascript
class Car {
    constructor(model) {
        this.model = model;
    }
    info() {
        console.log(`Car Model: ${this.model}`);
    }
}

class CarFactory {
    static createCar(model) {
        return new Car(model);
    }
}

const car1 = CarFactory.createCar("Tesla Model S");
car1.info(); // Outputs: Car Model: Tesla Model S
```

## 5. Proxy Pattern
The Proxy Pattern is used to control access to an object by providing a placeholder that intercepts interactions.

### Example:
```javascript
const handler = {
    get: function(target, prop) {
        return prop in target ? target[prop] : "Property does not exist";
    },
    set: function(target, prop, value) {
        if (typeof value === "string") {
            target[prop] = value;
        } else {
            console.log("Only string values are allowed");
        }
    }
};

const person = new Proxy({}, handler);
person.name = "John Doe";
console.log(person.name); // John Doe
console.log(person.age); // Property does not exist
```

## Complex Questions

### 6. Implement an Event Emitter in JavaScript
An Event Emitter allows different parts of an application to communicate by subscribing and emitting events.

### Example:
```javascript
class EventEmitter {
    constructor() {
        this.events = {};
    }
    on(event, listener) {
        if (!this.events[event]) {
            this.events[event] = [];
        }
        this.events[event].push(listener);
    }
    emit(event, data) {
        if (this.events[event]) {
            this.events[event].forEach(listener => listener(data));
        }
    }
    off(event, listener) {
        if (this.events[event]) {
            this.events[event] = this.events[event].filter(l => l !== listener);
        }
    }
}

const emitter = new EventEmitter();
const greet = name => console.log(`Hello, ${name}!`);

emitter.on("greet", greet);
emitter.emit("greet", "Alice"); // Outputs: Hello, Alice!
emitter.off("greet", greet);
```

### 7. Implement a Custom State Management System in JavaScript
A simple state management system can be built using the Observer Pattern.

### Example:
```javascript
class Store {
    constructor(initialState = {}) {
        this.state = initialState;
        this.listeners = [];
    }
    getState() {
        return this.state;
    }
    subscribe(listener) {
        this.listeners.push(listener);
    }
    dispatch(action) {
        this.state = { ...this.state, ...action };
        this.listeners.forEach(listener => listener(this.state));
    }
}

const store = new Store({ count: 0 });
store.subscribe(newState => console.log("State updated:", newState));

store.dispatch({ count: 1 }); // Outputs: State updated: { count: 1 }
store.dispatch({ count: 2 }); // Outputs: State updated: { count: 2 }
```
# JavaScript Security

## Common JavaScript Security Vulnerabilities
JavaScript applications are vulnerable to various security threats, including:

1. **Cross-Site Scripting (XSS)** - Injection of malicious scripts into web pages.
2. **Cross-Site Request Forgery (CSRF)** - Unauthorized actions performed on behalf of an authenticated user.
3. **Insecure APIs** - Improper authentication and exposure of sensitive data.
4. **Clickjacking** - Tricking users into clicking on malicious elements.
5. **Injection Attacks** - SQL Injection, NoSQL Injection, and Command Injection attacks.
6. **Prototype Pollution** - Manipulating JavaScript object prototypes to alter application behavior.
7. **CORS Misconfiguration** - Allowing unauthorized cross-origin requests.

## What is XSS (Cross-Site Scripting), and How Can It Be Prevented?
XSS allows attackers to inject malicious scripts into web pages viewed by other users. This can be prevented by:
- Escaping user input before rendering.
- Using Content Security Policy (CSP) to restrict script execution.
- Implementing input validation and sanitization.
- Avoiding `innerHTML` and using `textContent` instead.
- Using HTTP-only cookies to prevent access to session tokens.

## What is CSRF (Cross-Site Request Forgery), and How Can You Prevent It?
CSRF exploits authenticated users by tricking them into performing unauthorized actions. Prevention methods include:
- Using CSRF tokens to validate legitimate requests.
- Implementing SameSite cookies (`SameSite=Strict` or `SameSite=Lax`).
- Requiring re-authentication for sensitive actions.
- Validating the `Origin` and `Referer` headers on the server.

## What is CORS, and How Does It Work?
Cross-Origin Resource Sharing (CORS) is a security feature that controls which origins can access server resources. Key points:
- Defined using the `Access-Control-Allow-Origin` header.
- Supports whitelisting of allowed domains.
- Uses `Access-Control-Allow-Methods` to specify allowed HTTP methods.
- Preflight requests (`OPTIONS`) are used for non-simple requests.

Example CORS policy in Express.js:
```javascript
const cors = require('cors');
const app = require('express')();
app.use(cors({ origin: 'https://trusted-site.com' }));
```

## What Are the Security Risks of `eval()` in JavaScript?
Using `eval()` can introduce serious security risks, including:
- **Code Injection** - Attackers can execute arbitrary JavaScript.
- **Performance Issues** - `eval()` prevents optimizations and is slow.
- **Scope Pollution** - Variables inside `eval()` can leak into the surrounding scope.

### Safe Alternative:
Instead of `eval()`, use `JSON.parse()` or `Function()` for controlled execution.
```javascript
// Unsafe
eval("alert('Hacked!')");

// Safe alternative
const safeFunction = new Function("return 'Safe execution'");
safeFunction();
```

## How Would You Implement a Content Security Policy (CSP) in a JavaScript Application?
CSP helps prevent XSS attacks by restricting script execution. Implement it via HTTP headers:
```plaintext
Content-Security-Policy: default-src 'self'; script-src 'self' https://apis.example.com; object-src 'none';
```

Example in Express.js:
```javascript
const helmet = require('helmet');
const app = require('express')();
app.use(
  helmet.contentSecurityPolicy({
    directives: {
      defaultSrc: ["'self'"],
      scriptSrc: ["'self'", "https://apis.example.com"],
      objectSrc: ["'none'"]
    }
  })
);
```

## How Do You Secure a JWT Authentication System in a JavaScript App?
JSON Web Tokens (JWT) must be handled securely to prevent token theft and misuse. Best practices include:
- **Use Secure Storage**: Store JWTs in HTTP-only cookies instead of localStorage.
- **Set Expiry Time**: Use short-lived tokens and refresh tokens.
- **Verify Tokens**: Validate JWTs on the server using a secret key.
- **Use Strong Signing Algorithm**: Prefer `RS256` over `HS256`.
- **Restrict Token Usage**: Bind tokens to specific IP addresses or devices.
- **Implement Blacklisting**: Revoke compromised tokens.

Example JWT verification in Node.js:
```javascript
const jwt = require('jsonwebtoken');
const secretKey = 'superSecretKey';

function verifyToken(token) {
  try {
    return jwt.verify(token, secretKey);
  } catch (error) {
    return null;
  }
}
```

## Bonus: JavaScript Advanced Challenges

### Algorithmic Problems
1. **Find the longest substring without repeating characters.**
   ```js
   function longestUniqueSubstring(s) {
     let set = new Set();
     let left = 0, maxLength = 0;
     for (let right = 0; right < s.length; right++) {
       while (set.has(s[right])) {
         set.delete(s[left]);
         left++;
       }
       set.add(s[right]);
       maxLength = Math.max(maxLength, right - left + 1);
     }
     return maxLength;
   }
   ```

2. **Implement a LRU (Least Recently Used) Cache in JavaScript.**
   ```js
   class LRUCache {
     constructor(capacity) {
       this.capacity = capacity;
       this.cache = new Map();
     }
     get(key) {
       if (!this.cache.has(key)) return -1;
       let value = this.cache.get(key);
       this.cache.delete(key);
       this.cache.set(key, value);
       return value;
     }
     put(key, value) {
       if (this.cache.has(key)) this.cache.delete(key);
       this.cache.set(key, value);
       if (this.cache.size > this.capacity) this.cache.delete(this.cache.keys().next().value);
     }
   }
   ```

3. **Flatten a deeply nested array without using built-in functions.**
   ```js
   function flattenArray(arr) {
     let result = [];
     function flatten(subArr) {
       for (let item of subArr) {
         if (Array.isArray(item)) flatten(item);
         else result.push(item);
       }
     }
     flatten(arr);
     return result;
   }
   ```

4. **Create a function that performs deep comparison between two objects.**
   ```js
   function deepEqual(obj1, obj2) {
     if (obj1 === obj2) return true;
     if (typeof obj1 !== 'object' || typeof obj2 !== 'object' || obj1 === null || obj2 === null) return false;
     let keys1 = Object.keys(obj1), keys2 = Object.keys(obj2);
     if (keys1.length !== keys2.length) return false;
     return keys1.every(key => deepEqual(obj1[key], obj2[key]));
   }
   ```

5. **Write a function to find the intersection of two arrays.**
   ```js
   function arrayIntersection(arr1, arr2) {
     return arr1.filter(value => arr2.includes(value));
   }
   ```

6. **Reverse a linked list using JavaScript.**
   ```js
   class ListNode {
     constructor(value) {
       this.value = value;
       this.next = null;
     }
   }
   function reverseLinkedList(head) {
     let prev = null, current = head;
     while (current) {
       let next = current.next;
       current.next = prev;
       prev = current;
       current = next;
     }
     return prev;
   }
   ```

7. **Create a function that implements auto-complete search efficiently.**
   ```js
   class TrieNode {
     constructor() {
       this.children = {};
       this.isEndOfWord = false;
     }
   }
   class Trie {
     constructor() {
       this.root = new TrieNode();
     }
     insert(word) {
       let node = this.root;
       for (let char of word) {
         if (!node.children[char]) node.children[char] = new TrieNode();
         node = node.children[char];
       }
       node.isEndOfWord = true;
     }
     search(prefix) {
       let node = this.root;
       for (let char of prefix) {
         if (!node.children[char]) return [];
         node = node.children[char];
       }
       return this.getWords(node, prefix);
     }
     getWords(node, prefix) {
       let words = [];
       if (node.isEndOfWord) words.push(prefix);
       for (let char in node.children) {
         words.push(...this.getWords(node.children[char], prefix + char));
       }
       return words;
     }
   }
   ```

8. **Implement a retry mechanism for failed API calls.**
   ```js
   async function fetchWithRetry(url, retries = 3) {
     for (let i = 0; i < retries; i++) {
       try {
         let response = await fetch(url);
         if (!response.ok) throw new Error("Request failed");
         return await response.json();
       } catch (error) {
         if (i === retries - 1) throw error;
       }
     }
   }
   ```

9. **Build a custom event loop implementation.**
   ```js
   class EventLoop {
     constructor() {
       this.queue = [];
     }
     enqueue(task) {
       this.queue.push(task);
     }
     run() {
       while (this.queue.length) {
         let task = this.queue.shift();
         task();
       }
     }
   }
   ```

10. **Design a debounce function that supports immediate execution.**
    ```js
    function debounce(func, wait, immediate) {
      let timeout;
      return function (...args) {
        let callNow = immediate && !timeout;
        clearTimeout(timeout);
        timeout = setTimeout(() => timeout = null, wait);
        if (callNow) func.apply(this, args);
      };
    }
    ```

## Need any thing else?
If you need any thing else for any of these questions, feel free to ask! 🚀


## What is the difference between `var`, `let`, and `const`?
| Feature   | var  | let  | const |
|-----------|------|------|-------|
| Scope     | Function | Block | Block |
| Hoisting  | Yes (initialized as `undefined`) | Yes (not initialized) | Yes (not initialized) |
| Reassignable | Yes | Yes | No |

```javascript
var a = 10;  // Function-scoped
let b = 20;  // Block-scoped
const c = 30; // Block-scoped, cannot be reassigned
```

## What is an Immediately Invoked Function Expression (IIFE)?
An **IIFE** is a function that runs immediately after being defined.

```javascript
(function() {
    console.log("I am an IIFE");
})();
```

## What are promises in JavaScript?
A **Promise** represents a value that may be available now, in the future, or never. It has three states:
- **Pending**: Initial state
- **Resolved (Fulfilled)**: Operation completed successfully
- **Rejected**: Operation failed

```javascript
const promise = new Promise((resolve, reject) => {
    setTimeout(() => resolve("Success"), 2000);
});
promise.then(console.log).catch(console.error);
```

## What is the difference between `map()`, `filter()`, and `reduce()`?
- `map()`: Transforms each element in an array.
- `filter()`: Returns elements that satisfy a condition.
- `reduce()`: Reduces an array to a single value.

```javascript
const numbers = [1, 2, 3, 4];
const doubled = numbers.map(n => n * 2); // [2, 4, 6, 8]
const evens = numbers.filter(n => n % 2 === 0); // [2, 4]
const sum = numbers.reduce((acc, n) => acc + n, 0); // 10
```

## What is `this` in JavaScript?
The value of `this` depends on the context:
- **Global Scope**: `this` refers to the global object (`window` in browsers, `global` in Node.js).
- **Object Method**: `this` refers to the calling object.
- **Arrow Function**: `this` is lexically bound (inherits from the surrounding scope).

```javascript
const obj = {
    name: "John",
    sayHello: function() { console.log(this.name); } // John
};
const arrowFunc = () => console.log(this); // Lexical binding
```

## How does `async/await` work?
`async` and `await` make handling promises easier by allowing asynchronous code to be written like synchronous code.

```javascript
async function fetchData() {
    try {
        let response = await fetch('https://jsonplaceholder.typicode.com/todos/1');
        let data = await response.json();
        console.log(data);
    } catch (error) {
        console.error(error);
    }
}
fetchData();
```

## How can you deep clone an object in JavaScript?
```javascript
const obj = { a: 1, b: { c: 2 } };
const deepClone = JSON.parse(JSON.stringify(obj));
```

## 12. Explain debouncing and throttling.
- **Debouncing**: Ensures a function is executed only after a specified delay.
- **Throttling**: Ensures a function executes at most once in a specified interval.

```javascript
function debounce(func, delay) {
    let timeout;
    return function(...args) {
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(this, args), delay);
    };
}

function throttle(func, limit) {
    let inThrottle;
    return function(...args) {
        if (!inThrottle) {
            func.apply(this, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}
```

## 13. What is the difference between `call()`, `apply()`, and `bind()`?
- `call()`: Calls a function with `this` and arguments passed individually.
- `apply()`: Calls a function with `this` and arguments as an array.
- `bind()`: Returns a new function with `this` permanently set.

```javascript
function greet(greeting) {
    console.log(greeting + ' ' + this.name);
}
const user = { name: 'Alice' };
greet.call(user, 'Hello'); // Hello Alice
greet.apply(user, ['Hi']); // Hi Alice
const newGreet = greet.bind(user, 'Hey');
newGreet(); // Hey Alice
```

## 14. How do you check if an object is an array?
```javascript
console.log(Array.isArray([1, 2, 3])); // true
```
