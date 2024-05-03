const R = "val", w = "obj", g = "arr", y = "str", b = "num", S = "bol", _ = "nll", d = "chr", P = "int", K = "com", O = "col", i = "qot", T = "lbkt", Y = "rbkt", C = "lbrc", I = "rbrc", N = "ws", D = "wss", A = {
  VALUE_KEY: R,
  OBJECT_KEY: w,
  ARRAY_KEY: g,
  STRING_KEY: y,
  NUMBER_KEY: b,
  BOOLEAN_KEY: S,
  NULL_KEY: _,
  CHAR_KEY: d,
  INTEGER_KEY: P,
  COMMA_KEY: K,
  COLON_KEY: O,
  QUOTE_KEY: i,
  LEFT_BRACKET_KEY: T,
  RIGHT_BRACKET_KEY: Y,
  LEFT_BRACE_KEY: C,
  RIGHT_BRACE_KEY: I,
  WHITESPACE_KEY: N,
  WHITESPACE_REPEATING_KEY: D
}, x = (t) => (t >= 26 ? x((t / 26 >> 0) - 1) : "") + "abcdefghijklmnopqrstuvwxyz"[t % 26 >> 0], J = /{{(.*?)}}/g, p = (t) => {
  if (typeof t != "string")
    throw new Error(`Expected string for ${JSON.stringify(t)}`);
  return t.trim().replace(J, (e, n) => {
    const o = A[n];
    if (!o)
      throw new Error(`Unknown key ${n} for def ${t}`);
    return o;
  });
}, V = `"[" ({{VALUE_KEY}} ("," {{VALUE_KEY}})*)? "]"
`, q = `"{" ({{STRING_KEY}} ":" {{VALUE_KEY}} ("," {{STRING_KEY}} ":" {{VALUE_KEY}})*)? "}" 
`, z = `  "\\"" ({{CHAR_KEY}})* "\\""
`, Q = `("-"? ([0-9] | [1-9] [0-9]*)) ("." [0]+)? 
`, X = `("-"? ([0-9] | [1-9] [0-9]*)) ("." [0-9]+)? ([eE] [-+]? [0-9]+)?
`, Z = `"null"
`, tt = `"true" | "false"
`, et = `(
  [^"\\\\\\x7F\\x00-\\x1F] |
   "\\\\" (["\\\\/bfnrt] | "u" [0-9a-fA-F] [0-9a-fA-F] [0-9a-fA-F] [0-9a-fA-F]) # escapes
  )
`, nt = `[ \\t\\n]
`, ot = `({{WHITESPACE_KEY}} {{WHITESPACE_REPEATING_KEY}})?
`, rt = p(V), st = p(q), it = p(X), ct = p(Q), ft = p(z), lt = p(tt), ut = p(Z), pt = p(et), Et = p(nt), at = p(ot), dt = `${w} | ${g} | ${y} | ${b} | ${S} | ${_}`, $t = [
  `${R} ::= ${dt}`,
  `${w} ::= ${st}`,
  `${g} ::= ${rt}`,
  `${y} ::= ${ft}`,
  `${b} ::= ${it}`,
  `${S} ::= ${lt}`,
  `${_} ::= ${ut}`,
  `${d} ::= ${pt}`,
  `${P} ::= ${ct}`,
  `${K} ::= ","`,
  `${O} ::= ":"`,
  `${i} ::= "\\""`,
  `${T} ::= "["`,
  `${Y} ::= "]"`,
  `${C} ::= "{"`,
  `${I} ::= "}"`,
  `${N} ::= ${Et}`,
  `${D} ::= ${at}`
], c = (...t) => E(" ", ...t), E = (t, ...e) => e.filter(Boolean).join(t), yt = (t) => {
  const e = [];
  for (const [n, o] of t) {
    if (o === "")
      throw new Error("Key cannot be an empty string");
    if (n === "")
      throw new Error("Rule cannot be an empty string");
    e.push(`${o} ::= ${n}`);
  }
  return E(
    `
`,
    ...e,
    ...$t
  );
}, _t = (t, e, n) => E(
  "",
  e ? "ws" : void 0,
  t,
  n ? "ws" : void 0
), At = (t, e) => {
  if (t < 0 || !Number.isInteger(t))
    throw new Error("n must be a non-negative integer");
  const n = [];
  for (let o = 0; o < t; o++)
    n.push(e);
  return c(...n);
}, L = (t) => t.whitespace !== 1 / 0 ? t.addRule(At(
  t.whitespace,
  `(${N})?`
)) : D, Rt = (t, e, n, o) => c(
  n ? L(t) : void 0,
  e,
  o ? L(t) : void 0
);
class wt {
  #t = /* @__PURE__ */ new Map();
  fixedOrder;
  // whitespace can be Infinity or an integer greater than or equal to 0.
  whitespace;
  constructor({ whitespace: e = 1, fixedOrder: n = !1 } = {}) {
    if (e < 0)
      throw new Error("Whitespace must be greater than or equal to 0. It can also be infinity.");
    this.whitespace = e, this.fixedOrder = n;
  }
  getConst = (e, {
    left: n = !0,
    right: o = !0
  } = {}) => this.whitespace !== 0 ? this.addRule(
    Rt(this, e, n, o),
    _t(e, n, o)
  ) : e;
  addRule = (e, n) => {
    const o = n || (this.#t.get(e) ?? `x${x(this.#t.size)}`);
    return this.#t.set(e, o), o;
  };
  get grammar() {
    return yt(this.#t.entries());
  }
}
const $ = (t) => typeof t == "object" && t !== null, gt = (t) => $(t) && "type" in t && Array.isArray(t.type), U = (t) => $(t) && "enum" in t, B = (t) => $(t) && "const" in t, Gt = (t) => $(t) && "type" in t && t.type === "object", bt = (t) => typeof t == "object" && Object.keys(t).filter((e) => e !== "$schema").length === 0, St = (t) => $(t) && "$schema" in t && t.$schema !== void 0, Kt = (t) => !("items" in t) || t.items === void 0, Ot = (t) => "items" in t && typeof t.items == "boolean", Mt = (t) => "items" in t && typeof t.items == "object" && Array.isArray(t.items.type) === !1, kt = (t) => "items" in t && typeof t.items == "object" && Array.isArray(t.items.type) === !0, ht = (t) => $(t) && "type" in t && t.type === "string", mt = (t) => $(t) && "type" in t && (t.type === "number" || t.type === "integer"), G = (t) => [
  i,
  `"${t.const}"`,
  i
], Pt = [
  "prefixItems",
  "unevaluatedItems",
  "contains",
  "minContains",
  "maxContains",
  "minItems",
  "maxItems",
  "uniqueItems"
], Tt = (t, e) => {
  for (const r of Pt)
    if (e[r] !== void 0)
      throw new Error(`${r} is not supported`);
  if (Ot(e))
    throw new Error("boolean items is not supported, because prefixItems is not supported");
  if (Kt(e))
    return g;
  const n = [].concat(e.items.type).map((r) => A[`${r.toUpperCase()}_KEY`] ?? r), o = n.length > 1 ? t.addRule(E(" | ", ...n)) : n[0];
  return c(
    t.getConst(T, { left: !1 }),
    `(${o} (${t.getConst(K)} ${o})*)?`,
    t.getConst(Y, { right: !1 })
  );
}, Yt = (t, e = []) => {
  const n = [];
  function o(f, l) {
    f.length > 0 && n.push([...f]);
    for (let u = 0; u < l.length; u++)
      f.push(l[u]), o(f, l.slice(0, u).concat(l.slice(u + 1))), f.pop();
  }
  return o([], t), e.length === 0 ? n : n.filter((f) => {
    let l = !0;
    for (const u of e)
      if (!f.includes(u)) {
        l = !1;
        break;
      }
    return l;
  });
}, Ct = (t, e) => e(t.enum.map((n) => c(i, `"${n}"`, i)).join(" | ")), It = (t) => {
  const e = [
    t,
    i,
    y,
    i,
    O,
    R
  ];
  return `(${c(
    ...e,
    `(${c(...e)})*`
  )})?`;
}, Nt = [
  "patternProperties",
  "allOf",
  "unevaluatedProperties",
  "propertyNames",
  "minProperties",
  "maxProperties"
], Dt = (t, e) => B(e) ? G(e) : U(e) ? [Ct(e, t.addRule)] : [M(t, e)], jt = (t, e) => {
  for (const f of Nt)
    if (f in e)
      throw new Error(`${f} is not supported`);
  const { additionalProperties: n = !0, properties: o, required: r = [] } = e;
  if (o !== void 0 && typeof o == "object") {
    const f = t.getConst(O), l = t.getConst(C, { left: !1 }), u = t.getConst(I, { right: !1 }), h = t.getConst(K, { left: !1 }), j = n ? t.addRule(It(h)) : void 0, v = Object.entries(o).map(([s, a]) => ({
      rule: t.addRule(c(
        i,
        `"${s}"`,
        i,
        f,
        ...Dt(t, a)
      )),
      key: s
    })), k = v.reduce((s, { rule: a, key: H }) => ({
      ...s,
      [H]: a
    }), {}), m = v.map(({ rule: s }) => s);
    if (t.fixedOrder)
      return c(
        l,
        `(${E(
          ` ${h} `,
          ...m.map((s, a) => a === m.length - 1 && n ? c(s, j) : s)
        )})`,
        u
      );
    const F = r.map((s) => k[s]), W = Yt(m, F).map((s) => n ? s.map((a) => c(a, j)) : s).map((s) => s.length > 1 ? t.addRule(
      E(` ${h} `, ...s)
    ) : s[0]);
    return c(
      l,
      `(${E(" | ", ...W)})${r.length > 0 ? "" : "?"}`,
      u
    );
  }
  return w;
}, vt = (t) => {
  const { format: e, pattern: n, minLength: o, maxLength: r } = t;
  if (n !== void 0)
    throw new Error("pattern is not supported");
  if (e !== void 0)
    throw new Error("format is not supported");
  if (o !== void 0 && r !== void 0) {
    if (o > r)
      throw new Error("minLength must be less than or equal to maxLength");
    return c(
      i,
      Array(o).fill(d).join(" "),
      Array(r - o).fill(`(${d})?`).join(" "),
      i
    );
  } else {
    if (r === void 0 && o !== void 0)
      return c(
        i,
        Array(o - 1).fill(d).join(" "),
        `(${d})+`,
        i
      );
    if (o === void 0 && r !== void 0)
      return c(
        i,
        `${Array(r).fill(`(${d})?`).join(" ")}`,
        i
      );
  }
  return y;
}, Lt = [
  "exclusiveMinimum",
  "exclusiveMaximum",
  "multipleOf",
  "minimum",
  "maximum"
], xt = (t) => {
  for (const n of Lt)
    if (t[n] !== void 0)
      throw new Error(`${n} is not supported`);
  const { type: e } = t;
  return e === "number" ? b : P;
}, M = (t, e) => {
  const { type: n } = e;
  if (n === "boolean")
    return S;
  if (n === "null")
    return _;
  if (ht(e))
    return vt(e);
  if (mt(e))
    return xt(e);
  if (n === "array")
    return Tt(t, e);
  if (n === "object")
    return jt(t, e);
  throw new Error(`type for schema ${JSON.stringify(e)} is not supported`);
}, Ut = (t, e, n) => {
  gt(e) ? t.addRule(
    E(
      " | ",
      ...e.type.map((o) => {
        const r = `${o.toUpperCase()}_KEY`;
        if (!(r in A))
          throw new Error(`Unknown type ${o} for schema ${JSON.stringify(e)}`);
        return A[r];
      })
    ),
    n
  ) : U(e) ? t.addRule(
    E(
      " | ",
      ...e.enum.map((o) => JSON.stringify(o)).map((o) => o === "null" ? _ : JSON.stringify(o))
    ),
    n
  ) : B(e) ? t.addRule(
    c(...G(e)),
    n
  ) : t.addRule(
    M(t, e),
    n
  );
}, Bt = 'root ::= ""';
function Ft(t, e) {
  if (t == null)
    throw new Error("Bad schema provided");
  if (t === !1)
    return Bt;
  if (t !== !0 && St(t) && t.$schema !== "https://json-schema.org/draft/2020-12/schema")
    throw new Error(`Unsupported schema version: ${t.$schema}`);
  const n = new wt(e);
  return t === !0 || bt(t) ? n.addRule(R, "root") : Ut(n, t, "root"), n.grammar;
}
export {
  Ft as default,
  St as hasDollarSchemaProp,
  bt as isEmptyObject,
  kt as isSchemaArrayMultipleItemsType,
  Mt as isSchemaArraySingularItemsType,
  Ot as isSchemaArrayWithBooleanItemsType,
  Kt as isSchemaArrayWithoutItems,
  B as isSchemaConst,
  U as isSchemaEnum,
  gt as isSchemaMultipleBasicTypes,
  mt as isSchemaNumber,
  Gt as isSchemaObject,
  ht as isSchemaString
};
//# sourceMappingURL=index.js.map
