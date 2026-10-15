// Script-level regression only: these stub APIs do not emulate a physical FLX10.
const fs = require('fs');
const vm = require('vm');
const assert = require('assert/strict');
if (!process.argv[2]) throw Error('Usage: node tests/test_mixxx_mapping.js PATH-TO-MAPPING.js');
const state = new Map();
const messages = [];
const context = {
    console: {log() {}}, print() {},
    midi: {sendShortMsg(...args) { messages.push(args); }},
    engine: {
        getValue(g, k) { return state.get(g + ',' + k) || 0; },
        setValue(g, k, v) { state.set(g + ',' + k, v); },
        makeConnection() { return {trigger() {}, disconnect() {}}; },
        beginTimer() { return 1; }, stopTimer() {},
        softTakeover() {}, softTakeoverIgnoreNextValue() {},
    },
};
vm.createContext(context);
vm.runInContext(fs.readFileSync(process.argv[2], 'utf8'), context);
context.PioneerDDJFLX10.init('test');
for (let deck = 1; deck <= 4; deck++) {
    const group = '[Channel' + deck + ']';
    for (const [midiValue, expected] of [[0, 1], [127, -1]]) {
        context.PioneerDDJFLX10.rate_msb(deck - 1, 0, midiValue, 0xB0 + deck - 1, group);
        context.PioneerDDJFLX10.rate_lsb(deck - 1, 32, midiValue, 0xB0 + deck - 1, group);
        assert.equal(state.get(group + ',rate'), expected);
    }
}
assert(messages.length > 0);
console.log('PASS: MIDI-only init and eight pitch-fader endpoints (stub APIs; no hardware).');
