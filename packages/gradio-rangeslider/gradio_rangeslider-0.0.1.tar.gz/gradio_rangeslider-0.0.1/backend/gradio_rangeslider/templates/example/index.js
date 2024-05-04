const {
  SvelteComponent: _,
  attr: g,
  detach: o,
  element: r,
  init: m,
  insert: v,
  noop: f,
  safe_not_equal: y,
  toggle_class: i
} = window.__gradio__svelte__internal;
function b(n) {
  let e;
  return {
    c() {
      e = r("div"), e.textContent = `[${/*min*/
      n[2]}, ${/*max*/
      n[3]}]`, g(e, "class", "svelte-1gecy8w"), i(
        e,
        "table",
        /*type*/
        n[0] === "table"
      ), i(
        e,
        "gallery",
        /*type*/
        n[0] === "gallery"
      ), i(
        e,
        "selected",
        /*selected*/
        n[1]
      );
    },
    m(t, l) {
      v(t, e, l);
    },
    p(t, [l]) {
      l & /*type*/
      1 && i(
        e,
        "table",
        /*type*/
        t[0] === "table"
      ), l & /*type*/
      1 && i(
        e,
        "gallery",
        /*type*/
        t[0] === "gallery"
      ), l & /*selected*/
      2 && i(
        e,
        "selected",
        /*selected*/
        t[1]
      );
    },
    i: f,
    o: f,
    d(t) {
      t && o(e);
    }
  };
}
function w(n, e, t) {
  let { value: l } = e, { type: s } = e, { selected: c = !1 } = e, [u, d] = l;
  return n.$$set = (a) => {
    "value" in a && t(4, l = a.value), "type" in a && t(0, s = a.type), "selected" in a && t(1, c = a.selected);
  }, [s, c, u, d, l];
}
class h extends _ {
  constructor(e) {
    super(), m(this, e, w, b, y, { value: 4, type: 0, selected: 1 });
  }
}
export {
  h as default
};
