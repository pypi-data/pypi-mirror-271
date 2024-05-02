// Fix to avoid ReferenceError: DragEvent is not defined
Object.defineProperty(window, 'DragEvent', {
  value: class DragEvent {},
});
