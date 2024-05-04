const {
  SvelteComponent: Ot,
  assign: Jt,
  create_slot: Xt,
  detach: Yt,
  element: Gt,
  get_all_dirty_from_scope: Rt,
  get_slot_changes: Ht,
  get_spread_update: Kt,
  init: Qt,
  insert: Ut,
  safe_not_equal: Wt,
  set_dynamic_element_data: Qe,
  set_style: A,
  toggle_class: K,
  transition_in: vt,
  transition_out: yt,
  update_slot_base: xt
} = window.__gradio__svelte__internal;
function $t(l) {
  let e, t, n;
  const i = (
    /*#slots*/
    l[18].default
  ), f = Xt(
    i,
    l,
    /*$$scope*/
    l[17],
    null
  );
  let a = [
    { "data-testid": (
      /*test_id*/
      l[7]
    ) },
    { id: (
      /*elem_id*/
      l[2]
    ) },
    {
      class: t = "block " + /*elem_classes*/
      l[3].join(" ") + " svelte-nl1om8"
    }
  ], r = {};
  for (let s = 0; s < a.length; s += 1)
    r = Jt(r, a[s]);
  return {
    c() {
      e = Gt(
        /*tag*/
        l[14]
      ), f && f.c(), Qe(
        /*tag*/
        l[14]
      )(e, r), K(
        e,
        "hidden",
        /*visible*/
        l[10] === !1
      ), K(
        e,
        "padded",
        /*padding*/
        l[6]
      ), K(
        e,
        "border_focus",
        /*border_mode*/
        l[5] === "focus"
      ), K(
        e,
        "border_contrast",
        /*border_mode*/
        l[5] === "contrast"
      ), K(e, "hide-container", !/*explicit_call*/
      l[8] && !/*container*/
      l[9]), A(
        e,
        "height",
        /*get_dimension*/
        l[15](
          /*height*/
          l[0]
        )
      ), A(e, "width", typeof /*width*/
      l[1] == "number" ? `calc(min(${/*width*/
      l[1]}px, 100%))` : (
        /*get_dimension*/
        l[15](
          /*width*/
          l[1]
        )
      )), A(
        e,
        "border-style",
        /*variant*/
        l[4]
      ), A(
        e,
        "overflow",
        /*allow_overflow*/
        l[11] ? "visible" : "hidden"
      ), A(
        e,
        "flex-grow",
        /*scale*/
        l[12]
      ), A(e, "min-width", `calc(min(${/*min_width*/
      l[13]}px, 100%))`), A(e, "border-width", "var(--block-border-width)");
    },
    m(s, o) {
      Ut(s, e, o), f && f.m(e, null), n = !0;
    },
    p(s, o) {
      f && f.p && (!n || o & /*$$scope*/
      131072) && xt(
        f,
        i,
        s,
        /*$$scope*/
        s[17],
        n ? Ht(
          i,
          /*$$scope*/
          s[17],
          o,
          null
        ) : Rt(
          /*$$scope*/
          s[17]
        ),
        null
      ), Qe(
        /*tag*/
        s[14]
      )(e, r = Kt(a, [
        (!n || o & /*test_id*/
        128) && { "data-testid": (
          /*test_id*/
          s[7]
        ) },
        (!n || o & /*elem_id*/
        4) && { id: (
          /*elem_id*/
          s[2]
        ) },
        (!n || o & /*elem_classes*/
        8 && t !== (t = "block " + /*elem_classes*/
        s[3].join(" ") + " svelte-nl1om8")) && { class: t }
      ])), K(
        e,
        "hidden",
        /*visible*/
        s[10] === !1
      ), K(
        e,
        "padded",
        /*padding*/
        s[6]
      ), K(
        e,
        "border_focus",
        /*border_mode*/
        s[5] === "focus"
      ), K(
        e,
        "border_contrast",
        /*border_mode*/
        s[5] === "contrast"
      ), K(e, "hide-container", !/*explicit_call*/
      s[8] && !/*container*/
      s[9]), o & /*height*/
      1 && A(
        e,
        "height",
        /*get_dimension*/
        s[15](
          /*height*/
          s[0]
        )
      ), o & /*width*/
      2 && A(e, "width", typeof /*width*/
      s[1] == "number" ? `calc(min(${/*width*/
      s[1]}px, 100%))` : (
        /*get_dimension*/
        s[15](
          /*width*/
          s[1]
        )
      )), o & /*variant*/
      16 && A(
        e,
        "border-style",
        /*variant*/
        s[4]
      ), o & /*allow_overflow*/
      2048 && A(
        e,
        "overflow",
        /*allow_overflow*/
        s[11] ? "visible" : "hidden"
      ), o & /*scale*/
      4096 && A(
        e,
        "flex-grow",
        /*scale*/
        s[12]
      ), o & /*min_width*/
      8192 && A(e, "min-width", `calc(min(${/*min_width*/
      s[13]}px, 100%))`);
    },
    i(s) {
      n || (vt(f, s), n = !0);
    },
    o(s) {
      yt(f, s), n = !1;
    },
    d(s) {
      s && Yt(e), f && f.d(s);
    }
  };
}
function el(l) {
  let e, t = (
    /*tag*/
    l[14] && $t(l)
  );
  return {
    c() {
      t && t.c();
    },
    m(n, i) {
      t && t.m(n, i), e = !0;
    },
    p(n, [i]) {
      /*tag*/
      n[14] && t.p(n, i);
    },
    i(n) {
      e || (vt(t, n), e = !0);
    },
    o(n) {
      yt(t, n), e = !1;
    },
    d(n) {
      t && t.d(n);
    }
  };
}
function tl(l, e, t) {
  let { $$slots: n = {}, $$scope: i } = e, { height: f = void 0 } = e, { width: a = void 0 } = e, { elem_id: r = "" } = e, { elem_classes: s = [] } = e, { variant: o = "solid" } = e, { border_mode: u = "base" } = e, { padding: c = !0 } = e, { type: b = "normal" } = e, { test_id: g = void 0 } = e, { explicit_call: v = !1 } = e, { container: V = !0 } = e, { visible: k = !0 } = e, { allow_overflow: N = !0 } = e, { scale: m = null } = e, { min_width: d = 0 } = e, L = b === "fieldset" ? "fieldset" : "div";
  const M = (w) => {
    if (w !== void 0) {
      if (typeof w == "number")
        return w + "px";
      if (typeof w == "string")
        return w;
    }
  };
  return l.$$set = (w) => {
    "height" in w && t(0, f = w.height), "width" in w && t(1, a = w.width), "elem_id" in w && t(2, r = w.elem_id), "elem_classes" in w && t(3, s = w.elem_classes), "variant" in w && t(4, o = w.variant), "border_mode" in w && t(5, u = w.border_mode), "padding" in w && t(6, c = w.padding), "type" in w && t(16, b = w.type), "test_id" in w && t(7, g = w.test_id), "explicit_call" in w && t(8, v = w.explicit_call), "container" in w && t(9, V = w.container), "visible" in w && t(10, k = w.visible), "allow_overflow" in w && t(11, N = w.allow_overflow), "scale" in w && t(12, m = w.scale), "min_width" in w && t(13, d = w.min_width), "$$scope" in w && t(17, i = w.$$scope);
  }, [
    f,
    a,
    r,
    s,
    o,
    u,
    c,
    g,
    v,
    V,
    k,
    N,
    m,
    d,
    L,
    M,
    b,
    i,
    n
  ];
}
class ll extends Ot {
  constructor(e) {
    super(), Qt(this, e, tl, el, Wt, {
      height: 0,
      width: 1,
      elem_id: 2,
      elem_classes: 3,
      variant: 4,
      border_mode: 5,
      padding: 6,
      type: 16,
      test_id: 7,
      explicit_call: 8,
      container: 9,
      visible: 10,
      allow_overflow: 11,
      scale: 12,
      min_width: 13
    });
  }
}
const {
  SvelteComponent: nl,
  attr: il,
  create_slot: fl,
  detach: sl,
  element: ol,
  get_all_dirty_from_scope: al,
  get_slot_changes: rl,
  init: ul,
  insert: _l,
  safe_not_equal: cl,
  transition_in: dl,
  transition_out: ml,
  update_slot_base: bl
} = window.__gradio__svelte__internal;
function gl(l) {
  let e, t;
  const n = (
    /*#slots*/
    l[1].default
  ), i = fl(
    n,
    l,
    /*$$scope*/
    l[0],
    null
  );
  return {
    c() {
      e = ol("div"), i && i.c(), il(e, "class", "svelte-1hnfib2");
    },
    m(f, a) {
      _l(f, e, a), i && i.m(e, null), t = !0;
    },
    p(f, [a]) {
      i && i.p && (!t || a & /*$$scope*/
      1) && bl(
        i,
        n,
        f,
        /*$$scope*/
        f[0],
        t ? rl(
          n,
          /*$$scope*/
          f[0],
          a,
          null
        ) : al(
          /*$$scope*/
          f[0]
        ),
        null
      );
    },
    i(f) {
      t || (dl(i, f), t = !0);
    },
    o(f) {
      ml(i, f), t = !1;
    },
    d(f) {
      f && sl(e), i && i.d(f);
    }
  };
}
function hl(l, e, t) {
  let { $$slots: n = {}, $$scope: i } = e;
  return l.$$set = (f) => {
    "$$scope" in f && t(0, i = f.$$scope);
  }, [i, n];
}
class wl extends nl {
  constructor(e) {
    super(), ul(this, e, hl, gl, cl, {});
  }
}
const {
  SvelteComponent: pl,
  attr: Ue,
  check_outros: kl,
  create_component: vl,
  create_slot: yl,
  destroy_component: ql,
  detach: ze,
  element: Cl,
  empty: Fl,
  get_all_dirty_from_scope: Ll,
  get_slot_changes: Sl,
  group_outros: zl,
  init: Ml,
  insert: Me,
  mount_component: Vl,
  safe_not_equal: Nl,
  set_data: Il,
  space: Zl,
  text: jl,
  toggle_class: ue,
  transition_in: we,
  transition_out: Ve,
  update_slot_base: Pl
} = window.__gradio__svelte__internal;
function We(l) {
  let e, t;
  return e = new wl({
    props: {
      $$slots: { default: [Bl] },
      $$scope: { ctx: l }
    }
  }), {
    c() {
      vl(e.$$.fragment);
    },
    m(n, i) {
      Vl(e, n, i), t = !0;
    },
    p(n, i) {
      const f = {};
      i & /*$$scope, info*/
      10 && (f.$$scope = { dirty: i, ctx: n }), e.$set(f);
    },
    i(n) {
      t || (we(e.$$.fragment, n), t = !0);
    },
    o(n) {
      Ve(e.$$.fragment, n), t = !1;
    },
    d(n) {
      ql(e, n);
    }
  };
}
function Bl(l) {
  let e;
  return {
    c() {
      e = jl(
        /*info*/
        l[1]
      );
    },
    m(t, n) {
      Me(t, e, n);
    },
    p(t, n) {
      n & /*info*/
      2 && Il(
        e,
        /*info*/
        t[1]
      );
    },
    d(t) {
      t && ze(e);
    }
  };
}
function Al(l) {
  let e, t, n, i;
  const f = (
    /*#slots*/
    l[2].default
  ), a = yl(
    f,
    l,
    /*$$scope*/
    l[3],
    null
  );
  let r = (
    /*info*/
    l[1] && We(l)
  );
  return {
    c() {
      e = Cl("span"), a && a.c(), t = Zl(), r && r.c(), n = Fl(), Ue(e, "data-testid", "block-info"), Ue(e, "class", "svelte-22c38v"), ue(e, "sr-only", !/*show_label*/
      l[0]), ue(e, "hide", !/*show_label*/
      l[0]), ue(
        e,
        "has-info",
        /*info*/
        l[1] != null
      );
    },
    m(s, o) {
      Me(s, e, o), a && a.m(e, null), Me(s, t, o), r && r.m(s, o), Me(s, n, o), i = !0;
    },
    p(s, [o]) {
      a && a.p && (!i || o & /*$$scope*/
      8) && Pl(
        a,
        f,
        s,
        /*$$scope*/
        s[3],
        i ? Sl(
          f,
          /*$$scope*/
          s[3],
          o,
          null
        ) : Ll(
          /*$$scope*/
          s[3]
        ),
        null
      ), (!i || o & /*show_label*/
      1) && ue(e, "sr-only", !/*show_label*/
      s[0]), (!i || o & /*show_label*/
      1) && ue(e, "hide", !/*show_label*/
      s[0]), (!i || o & /*info*/
      2) && ue(
        e,
        "has-info",
        /*info*/
        s[1] != null
      ), /*info*/
      s[1] ? r ? (r.p(s, o), o & /*info*/
      2 && we(r, 1)) : (r = We(s), r.c(), we(r, 1), r.m(n.parentNode, n)) : r && (zl(), Ve(r, 1, 1, () => {
        r = null;
      }), kl());
    },
    i(s) {
      i || (we(a, s), we(r), i = !0);
    },
    o(s) {
      Ve(a, s), Ve(r), i = !1;
    },
    d(s) {
      s && (ze(e), ze(t), ze(n)), a && a.d(s), r && r.d(s);
    }
  };
}
function Dl(l, e, t) {
  let { $$slots: n = {}, $$scope: i } = e, { show_label: f = !0 } = e, { info: a = void 0 } = e;
  return l.$$set = (r) => {
    "show_label" in r && t(0, f = r.show_label), "info" in r && t(1, a = r.info), "$$scope" in r && t(3, i = r.$$scope);
  }, [f, a, n, i];
}
class El extends pl {
  constructor(e) {
    super(), Ml(this, e, Dl, Al, Nl, { show_label: 0, info: 1 });
  }
}
const {
  SvelteComponent: Tl,
  append: De,
  attr: x,
  bubble: Ol,
  create_component: Jl,
  destroy_component: Xl,
  detach: qt,
  element: Ee,
  init: Yl,
  insert: Ct,
  listen: Gl,
  mount_component: Rl,
  safe_not_equal: Hl,
  set_data: Kl,
  set_style: _e,
  space: Ql,
  text: Ul,
  toggle_class: P,
  transition_in: Wl,
  transition_out: xl
} = window.__gradio__svelte__internal;
function xe(l) {
  let e, t;
  return {
    c() {
      e = Ee("span"), t = Ul(
        /*label*/
        l[1]
      ), x(e, "class", "svelte-1lrphxw");
    },
    m(n, i) {
      Ct(n, e, i), De(e, t);
    },
    p(n, i) {
      i & /*label*/
      2 && Kl(
        t,
        /*label*/
        n[1]
      );
    },
    d(n) {
      n && qt(e);
    }
  };
}
function $l(l) {
  let e, t, n, i, f, a, r, s = (
    /*show_label*/
    l[2] && xe(l)
  );
  return i = new /*Icon*/
  l[0]({}), {
    c() {
      e = Ee("button"), s && s.c(), t = Ql(), n = Ee("div"), Jl(i.$$.fragment), x(n, "class", "svelte-1lrphxw"), P(
        n,
        "small",
        /*size*/
        l[4] === "small"
      ), P(
        n,
        "large",
        /*size*/
        l[4] === "large"
      ), P(
        n,
        "medium",
        /*size*/
        l[4] === "medium"
      ), e.disabled = /*disabled*/
      l[7], x(
        e,
        "aria-label",
        /*label*/
        l[1]
      ), x(
        e,
        "aria-haspopup",
        /*hasPopup*/
        l[8]
      ), x(
        e,
        "title",
        /*label*/
        l[1]
      ), x(e, "class", "svelte-1lrphxw"), P(
        e,
        "pending",
        /*pending*/
        l[3]
      ), P(
        e,
        "padded",
        /*padded*/
        l[5]
      ), P(
        e,
        "highlight",
        /*highlight*/
        l[6]
      ), P(
        e,
        "transparent",
        /*transparent*/
        l[9]
      ), _e(e, "color", !/*disabled*/
      l[7] && /*_color*/
      l[12] ? (
        /*_color*/
        l[12]
      ) : "var(--block-label-text-color)"), _e(e, "--bg-color", /*disabled*/
      l[7] ? "auto" : (
        /*background*/
        l[10]
      )), _e(
        e,
        "margin-left",
        /*offset*/
        l[11] + "px"
      );
    },
    m(o, u) {
      Ct(o, e, u), s && s.m(e, null), De(e, t), De(e, n), Rl(i, n, null), f = !0, a || (r = Gl(
        e,
        "click",
        /*click_handler*/
        l[14]
      ), a = !0);
    },
    p(o, [u]) {
      /*show_label*/
      o[2] ? s ? s.p(o, u) : (s = xe(o), s.c(), s.m(e, t)) : s && (s.d(1), s = null), (!f || u & /*size*/
      16) && P(
        n,
        "small",
        /*size*/
        o[4] === "small"
      ), (!f || u & /*size*/
      16) && P(
        n,
        "large",
        /*size*/
        o[4] === "large"
      ), (!f || u & /*size*/
      16) && P(
        n,
        "medium",
        /*size*/
        o[4] === "medium"
      ), (!f || u & /*disabled*/
      128) && (e.disabled = /*disabled*/
      o[7]), (!f || u & /*label*/
      2) && x(
        e,
        "aria-label",
        /*label*/
        o[1]
      ), (!f || u & /*hasPopup*/
      256) && x(
        e,
        "aria-haspopup",
        /*hasPopup*/
        o[8]
      ), (!f || u & /*label*/
      2) && x(
        e,
        "title",
        /*label*/
        o[1]
      ), (!f || u & /*pending*/
      8) && P(
        e,
        "pending",
        /*pending*/
        o[3]
      ), (!f || u & /*padded*/
      32) && P(
        e,
        "padded",
        /*padded*/
        o[5]
      ), (!f || u & /*highlight*/
      64) && P(
        e,
        "highlight",
        /*highlight*/
        o[6]
      ), (!f || u & /*transparent*/
      512) && P(
        e,
        "transparent",
        /*transparent*/
        o[9]
      ), u & /*disabled, _color*/
      4224 && _e(e, "color", !/*disabled*/
      o[7] && /*_color*/
      o[12] ? (
        /*_color*/
        o[12]
      ) : "var(--block-label-text-color)"), u & /*disabled, background*/
      1152 && _e(e, "--bg-color", /*disabled*/
      o[7] ? "auto" : (
        /*background*/
        o[10]
      )), u & /*offset*/
      2048 && _e(
        e,
        "margin-left",
        /*offset*/
        o[11] + "px"
      );
    },
    i(o) {
      f || (Wl(i.$$.fragment, o), f = !0);
    },
    o(o) {
      xl(i.$$.fragment, o), f = !1;
    },
    d(o) {
      o && qt(e), s && s.d(), Xl(i), a = !1, r();
    }
  };
}
function en(l, e, t) {
  let n, { Icon: i } = e, { label: f = "" } = e, { show_label: a = !1 } = e, { pending: r = !1 } = e, { size: s = "small" } = e, { padded: o = !0 } = e, { highlight: u = !1 } = e, { disabled: c = !1 } = e, { hasPopup: b = !1 } = e, { color: g = "var(--block-label-text-color)" } = e, { transparent: v = !1 } = e, { background: V = "var(--background-fill-primary)" } = e, { offset: k = 0 } = e;
  function N(m) {
    Ol.call(this, l, m);
  }
  return l.$$set = (m) => {
    "Icon" in m && t(0, i = m.Icon), "label" in m && t(1, f = m.label), "show_label" in m && t(2, a = m.show_label), "pending" in m && t(3, r = m.pending), "size" in m && t(4, s = m.size), "padded" in m && t(5, o = m.padded), "highlight" in m && t(6, u = m.highlight), "disabled" in m && t(7, c = m.disabled), "hasPopup" in m && t(8, b = m.hasPopup), "color" in m && t(13, g = m.color), "transparent" in m && t(9, v = m.transparent), "background" in m && t(10, V = m.background), "offset" in m && t(11, k = m.offset);
  }, l.$$.update = () => {
    l.$$.dirty & /*highlight, color*/
    8256 && t(12, n = u ? "var(--color-accent)" : g);
  }, [
    i,
    f,
    a,
    r,
    s,
    o,
    u,
    c,
    b,
    v,
    V,
    k,
    n,
    g,
    N
  ];
}
class tn extends Tl {
  constructor(e) {
    super(), Yl(this, e, en, $l, Hl, {
      Icon: 0,
      label: 1,
      show_label: 2,
      pending: 3,
      size: 4,
      padded: 5,
      highlight: 6,
      disabled: 7,
      hasPopup: 8,
      color: 13,
      transparent: 9,
      background: 10,
      offset: 11
    });
  }
}
const {
  SvelteComponent: ln,
  append: Pe,
  attr: X,
  detach: nn,
  init: fn,
  insert: sn,
  noop: Be,
  safe_not_equal: on,
  set_style: Q,
  svg_element: Fe
} = window.__gradio__svelte__internal;
function an(l) {
  let e, t, n, i;
  return {
    c() {
      e = Fe("svg"), t = Fe("g"), n = Fe("path"), i = Fe("path"), X(n, "d", "M18,6L6.087,17.913"), Q(n, "fill", "none"), Q(n, "fill-rule", "nonzero"), Q(n, "stroke-width", "2px"), X(t, "transform", "matrix(1.14096,-0.140958,-0.140958,1.14096,-0.0559523,0.0559523)"), X(i, "d", "M4.364,4.364L19.636,19.636"), Q(i, "fill", "none"), Q(i, "fill-rule", "nonzero"), Q(i, "stroke-width", "2px"), X(e, "width", "100%"), X(e, "height", "100%"), X(e, "viewBox", "0 0 24 24"), X(e, "version", "1.1"), X(e, "xmlns", "http://www.w3.org/2000/svg"), X(e, "xmlns:xlink", "http://www.w3.org/1999/xlink"), X(e, "xml:space", "preserve"), X(e, "stroke", "currentColor"), Q(e, "fill-rule", "evenodd"), Q(e, "clip-rule", "evenodd"), Q(e, "stroke-linecap", "round"), Q(e, "stroke-linejoin", "round");
    },
    m(f, a) {
      sn(f, e, a), Pe(e, t), Pe(t, n), Pe(e, i);
    },
    p: Be,
    i: Be,
    o: Be,
    d(f) {
      f && nn(e);
    }
  };
}
class rn extends ln {
  constructor(e) {
    super(), fn(this, e, null, an, on, {});
  }
}
const un = [
  { color: "red", primary: 600, secondary: 100 },
  { color: "green", primary: 600, secondary: 100 },
  { color: "blue", primary: 600, secondary: 100 },
  { color: "yellow", primary: 500, secondary: 100 },
  { color: "purple", primary: 600, secondary: 100 },
  { color: "teal", primary: 600, secondary: 100 },
  { color: "orange", primary: 600, secondary: 100 },
  { color: "cyan", primary: 600, secondary: 100 },
  { color: "lime", primary: 500, secondary: 100 },
  { color: "pink", primary: 600, secondary: 100 }
], $e = {
  inherit: "inherit",
  current: "currentColor",
  transparent: "transparent",
  black: "#000",
  white: "#fff",
  slate: {
    50: "#f8fafc",
    100: "#f1f5f9",
    200: "#e2e8f0",
    300: "#cbd5e1",
    400: "#94a3b8",
    500: "#64748b",
    600: "#475569",
    700: "#334155",
    800: "#1e293b",
    900: "#0f172a",
    950: "#020617"
  },
  gray: {
    50: "#f9fafb",
    100: "#f3f4f6",
    200: "#e5e7eb",
    300: "#d1d5db",
    400: "#9ca3af",
    500: "#6b7280",
    600: "#4b5563",
    700: "#374151",
    800: "#1f2937",
    900: "#111827",
    950: "#030712"
  },
  zinc: {
    50: "#fafafa",
    100: "#f4f4f5",
    200: "#e4e4e7",
    300: "#d4d4d8",
    400: "#a1a1aa",
    500: "#71717a",
    600: "#52525b",
    700: "#3f3f46",
    800: "#27272a",
    900: "#18181b",
    950: "#09090b"
  },
  neutral: {
    50: "#fafafa",
    100: "#f5f5f5",
    200: "#e5e5e5",
    300: "#d4d4d4",
    400: "#a3a3a3",
    500: "#737373",
    600: "#525252",
    700: "#404040",
    800: "#262626",
    900: "#171717",
    950: "#0a0a0a"
  },
  stone: {
    50: "#fafaf9",
    100: "#f5f5f4",
    200: "#e7e5e4",
    300: "#d6d3d1",
    400: "#a8a29e",
    500: "#78716c",
    600: "#57534e",
    700: "#44403c",
    800: "#292524",
    900: "#1c1917",
    950: "#0c0a09"
  },
  red: {
    50: "#fef2f2",
    100: "#fee2e2",
    200: "#fecaca",
    300: "#fca5a5",
    400: "#f87171",
    500: "#ef4444",
    600: "#dc2626",
    700: "#b91c1c",
    800: "#991b1b",
    900: "#7f1d1d",
    950: "#450a0a"
  },
  orange: {
    50: "#fff7ed",
    100: "#ffedd5",
    200: "#fed7aa",
    300: "#fdba74",
    400: "#fb923c",
    500: "#f97316",
    600: "#ea580c",
    700: "#c2410c",
    800: "#9a3412",
    900: "#7c2d12",
    950: "#431407"
  },
  amber: {
    50: "#fffbeb",
    100: "#fef3c7",
    200: "#fde68a",
    300: "#fcd34d",
    400: "#fbbf24",
    500: "#f59e0b",
    600: "#d97706",
    700: "#b45309",
    800: "#92400e",
    900: "#78350f",
    950: "#451a03"
  },
  yellow: {
    50: "#fefce8",
    100: "#fef9c3",
    200: "#fef08a",
    300: "#fde047",
    400: "#facc15",
    500: "#eab308",
    600: "#ca8a04",
    700: "#a16207",
    800: "#854d0e",
    900: "#713f12",
    950: "#422006"
  },
  lime: {
    50: "#f7fee7",
    100: "#ecfccb",
    200: "#d9f99d",
    300: "#bef264",
    400: "#a3e635",
    500: "#84cc16",
    600: "#65a30d",
    700: "#4d7c0f",
    800: "#3f6212",
    900: "#365314",
    950: "#1a2e05"
  },
  green: {
    50: "#f0fdf4",
    100: "#dcfce7",
    200: "#bbf7d0",
    300: "#86efac",
    400: "#4ade80",
    500: "#22c55e",
    600: "#16a34a",
    700: "#15803d",
    800: "#166534",
    900: "#14532d",
    950: "#052e16"
  },
  emerald: {
    50: "#ecfdf5",
    100: "#d1fae5",
    200: "#a7f3d0",
    300: "#6ee7b7",
    400: "#34d399",
    500: "#10b981",
    600: "#059669",
    700: "#047857",
    800: "#065f46",
    900: "#064e3b",
    950: "#022c22"
  },
  teal: {
    50: "#f0fdfa",
    100: "#ccfbf1",
    200: "#99f6e4",
    300: "#5eead4",
    400: "#2dd4bf",
    500: "#14b8a6",
    600: "#0d9488",
    700: "#0f766e",
    800: "#115e59",
    900: "#134e4a",
    950: "#042f2e"
  },
  cyan: {
    50: "#ecfeff",
    100: "#cffafe",
    200: "#a5f3fc",
    300: "#67e8f9",
    400: "#22d3ee",
    500: "#06b6d4",
    600: "#0891b2",
    700: "#0e7490",
    800: "#155e75",
    900: "#164e63",
    950: "#083344"
  },
  sky: {
    50: "#f0f9ff",
    100: "#e0f2fe",
    200: "#bae6fd",
    300: "#7dd3fc",
    400: "#38bdf8",
    500: "#0ea5e9",
    600: "#0284c7",
    700: "#0369a1",
    800: "#075985",
    900: "#0c4a6e",
    950: "#082f49"
  },
  blue: {
    50: "#eff6ff",
    100: "#dbeafe",
    200: "#bfdbfe",
    300: "#93c5fd",
    400: "#60a5fa",
    500: "#3b82f6",
    600: "#2563eb",
    700: "#1d4ed8",
    800: "#1e40af",
    900: "#1e3a8a",
    950: "#172554"
  },
  indigo: {
    50: "#eef2ff",
    100: "#e0e7ff",
    200: "#c7d2fe",
    300: "#a5b4fc",
    400: "#818cf8",
    500: "#6366f1",
    600: "#4f46e5",
    700: "#4338ca",
    800: "#3730a3",
    900: "#312e81",
    950: "#1e1b4b"
  },
  violet: {
    50: "#f5f3ff",
    100: "#ede9fe",
    200: "#ddd6fe",
    300: "#c4b5fd",
    400: "#a78bfa",
    500: "#8b5cf6",
    600: "#7c3aed",
    700: "#6d28d9",
    800: "#5b21b6",
    900: "#4c1d95",
    950: "#2e1065"
  },
  purple: {
    50: "#faf5ff",
    100: "#f3e8ff",
    200: "#e9d5ff",
    300: "#d8b4fe",
    400: "#c084fc",
    500: "#a855f7",
    600: "#9333ea",
    700: "#7e22ce",
    800: "#6b21a8",
    900: "#581c87",
    950: "#3b0764"
  },
  fuchsia: {
    50: "#fdf4ff",
    100: "#fae8ff",
    200: "#f5d0fe",
    300: "#f0abfc",
    400: "#e879f9",
    500: "#d946ef",
    600: "#c026d3",
    700: "#a21caf",
    800: "#86198f",
    900: "#701a75",
    950: "#4a044e"
  },
  pink: {
    50: "#fdf2f8",
    100: "#fce7f3",
    200: "#fbcfe8",
    300: "#f9a8d4",
    400: "#f472b6",
    500: "#ec4899",
    600: "#db2777",
    700: "#be185d",
    800: "#9d174d",
    900: "#831843",
    950: "#500724"
  },
  rose: {
    50: "#fff1f2",
    100: "#ffe4e6",
    200: "#fecdd3",
    300: "#fda4af",
    400: "#fb7185",
    500: "#f43f5e",
    600: "#e11d48",
    700: "#be123c",
    800: "#9f1239",
    900: "#881337",
    950: "#4c0519"
  }
};
un.reduce(
  (l, { color: e, primary: t, secondary: n }) => ({
    ...l,
    [e]: {
      primary: $e[e][t],
      secondary: $e[e][n]
    }
  }),
  {}
);
function de(l) {
  let e = ["", "k", "M", "G", "T", "P", "E", "Z"], t = 0;
  for (; l > 1e3 && t < e.length - 1; )
    l /= 1e3, t++;
  let n = e[t];
  return (Number.isInteger(l) ? l : l.toFixed(1)) + n;
}
function Ne() {
}
function _n(l, e) {
  return l != l ? e == e : l !== e || l && typeof l == "object" || typeof l == "function";
}
const Ft = typeof window < "u";
let et = Ft ? () => window.performance.now() : () => Date.now(), Lt = Ft ? (l) => requestAnimationFrame(l) : Ne;
const be = /* @__PURE__ */ new Set();
function St(l) {
  be.forEach((e) => {
    e.c(l) || (be.delete(e), e.f());
  }), be.size !== 0 && Lt(St);
}
function cn(l) {
  let e;
  return be.size === 0 && Lt(St), {
    promise: new Promise((t) => {
      be.add(e = { c: l, f: t });
    }),
    abort() {
      be.delete(e);
    }
  };
}
const ce = [];
function dn(l, e = Ne) {
  let t;
  const n = /* @__PURE__ */ new Set();
  function i(r) {
    if (_n(l, r) && (l = r, t)) {
      const s = !ce.length;
      for (const o of n)
        o[1](), ce.push(o, l);
      if (s) {
        for (let o = 0; o < ce.length; o += 2)
          ce[o][0](ce[o + 1]);
        ce.length = 0;
      }
    }
  }
  function f(r) {
    i(r(l));
  }
  function a(r, s = Ne) {
    const o = [r, s];
    return n.add(o), n.size === 1 && (t = e(i, f) || Ne), r(l), () => {
      n.delete(o), n.size === 0 && t && (t(), t = null);
    };
  }
  return { set: i, update: f, subscribe: a };
}
function tt(l) {
  return Object.prototype.toString.call(l) === "[object Date]";
}
function Te(l, e, t, n) {
  if (typeof t == "number" || tt(t)) {
    const i = n - t, f = (t - e) / (l.dt || 1 / 60), a = l.opts.stiffness * i, r = l.opts.damping * f, s = (a - r) * l.inv_mass, o = (f + s) * l.dt;
    return Math.abs(o) < l.opts.precision && Math.abs(i) < l.opts.precision ? n : (l.settled = !1, tt(t) ? new Date(t.getTime() + o) : t + o);
  } else {
    if (Array.isArray(t))
      return t.map(
        (i, f) => Te(l, e[f], t[f], n[f])
      );
    if (typeof t == "object") {
      const i = {};
      for (const f in t)
        i[f] = Te(l, e[f], t[f], n[f]);
      return i;
    } else
      throw new Error(`Cannot spring ${typeof t} values`);
  }
}
function lt(l, e = {}) {
  const t = dn(l), { stiffness: n = 0.15, damping: i = 0.8, precision: f = 0.01 } = e;
  let a, r, s, o = l, u = l, c = 1, b = 0, g = !1;
  function v(k, N = {}) {
    u = k;
    const m = s = {};
    return l == null || N.hard || V.stiffness >= 1 && V.damping >= 1 ? (g = !0, a = et(), o = k, t.set(l = u), Promise.resolve()) : (N.soft && (b = 1 / ((N.soft === !0 ? 0.5 : +N.soft) * 60), c = 0), r || (a = et(), g = !1, r = cn((d) => {
      if (g)
        return g = !1, r = null, !1;
      c = Math.min(c + b, 1);
      const L = {
        inv_mass: c,
        opts: V,
        settled: !0,
        dt: (d - a) * 60 / 1e3
      }, M = Te(L, o, l, u);
      return a = d, o = l, t.set(l = M), L.settled && (r = null), !L.settled;
    })), new Promise((d) => {
      r.promise.then(() => {
        m === s && d();
      });
    }));
  }
  const V = {
    set: v,
    update: (k, N) => v(k(u, l), N),
    subscribe: t.subscribe,
    stiffness: n,
    damping: i,
    precision: f
  };
  return V;
}
const {
  SvelteComponent: mn,
  append: Y,
  attr: z,
  component_subscribe: nt,
  detach: bn,
  element: gn,
  init: hn,
  insert: wn,
  noop: it,
  safe_not_equal: pn,
  set_style: Le,
  svg_element: G,
  toggle_class: ft
} = window.__gradio__svelte__internal, { onMount: kn } = window.__gradio__svelte__internal;
function vn(l) {
  let e, t, n, i, f, a, r, s, o, u, c, b;
  return {
    c() {
      e = gn("div"), t = G("svg"), n = G("g"), i = G("path"), f = G("path"), a = G("path"), r = G("path"), s = G("g"), o = G("path"), u = G("path"), c = G("path"), b = G("path"), z(i, "d", "M255.926 0.754768L509.702 139.936V221.027L255.926 81.8465V0.754768Z"), z(i, "fill", "#FF7C00"), z(i, "fill-opacity", "0.4"), z(i, "class", "svelte-43sxxs"), z(f, "d", "M509.69 139.936L254.981 279.641V361.255L509.69 221.55V139.936Z"), z(f, "fill", "#FF7C00"), z(f, "class", "svelte-43sxxs"), z(a, "d", "M0.250138 139.937L254.981 279.641V361.255L0.250138 221.55V139.937Z"), z(a, "fill", "#FF7C00"), z(a, "fill-opacity", "0.4"), z(a, "class", "svelte-43sxxs"), z(r, "d", "M255.923 0.232622L0.236328 139.936V221.55L255.923 81.8469V0.232622Z"), z(r, "fill", "#FF7C00"), z(r, "class", "svelte-43sxxs"), Le(n, "transform", "translate(" + /*$top*/
      l[1][0] + "px, " + /*$top*/
      l[1][1] + "px)"), z(o, "d", "M255.926 141.5L509.702 280.681V361.773L255.926 222.592V141.5Z"), z(o, "fill", "#FF7C00"), z(o, "fill-opacity", "0.4"), z(o, "class", "svelte-43sxxs"), z(u, "d", "M509.69 280.679L254.981 420.384V501.998L509.69 362.293V280.679Z"), z(u, "fill", "#FF7C00"), z(u, "class", "svelte-43sxxs"), z(c, "d", "M0.250138 280.681L254.981 420.386V502L0.250138 362.295V280.681Z"), z(c, "fill", "#FF7C00"), z(c, "fill-opacity", "0.4"), z(c, "class", "svelte-43sxxs"), z(b, "d", "M255.923 140.977L0.236328 280.68V362.294L255.923 222.591V140.977Z"), z(b, "fill", "#FF7C00"), z(b, "class", "svelte-43sxxs"), Le(s, "transform", "translate(" + /*$bottom*/
      l[2][0] + "px, " + /*$bottom*/
      l[2][1] + "px)"), z(t, "viewBox", "-1200 -1200 3000 3000"), z(t, "fill", "none"), z(t, "xmlns", "http://www.w3.org/2000/svg"), z(t, "class", "svelte-43sxxs"), z(e, "class", "svelte-43sxxs"), ft(
        e,
        "margin",
        /*margin*/
        l[0]
      );
    },
    m(g, v) {
      wn(g, e, v), Y(e, t), Y(t, n), Y(n, i), Y(n, f), Y(n, a), Y(n, r), Y(t, s), Y(s, o), Y(s, u), Y(s, c), Y(s, b);
    },
    p(g, [v]) {
      v & /*$top*/
      2 && Le(n, "transform", "translate(" + /*$top*/
      g[1][0] + "px, " + /*$top*/
      g[1][1] + "px)"), v & /*$bottom*/
      4 && Le(s, "transform", "translate(" + /*$bottom*/
      g[2][0] + "px, " + /*$bottom*/
      g[2][1] + "px)"), v & /*margin*/
      1 && ft(
        e,
        "margin",
        /*margin*/
        g[0]
      );
    },
    i: it,
    o: it,
    d(g) {
      g && bn(e);
    }
  };
}
function yn(l, e, t) {
  let n, i;
  var f = this && this.__awaiter || function(g, v, V, k) {
    function N(m) {
      return m instanceof V ? m : new V(function(d) {
        d(m);
      });
    }
    return new (V || (V = Promise))(function(m, d) {
      function L(j) {
        try {
          w(k.next(j));
        } catch (S) {
          d(S);
        }
      }
      function M(j) {
        try {
          w(k.throw(j));
        } catch (S) {
          d(S);
        }
      }
      function w(j) {
        j.done ? m(j.value) : N(j.value).then(L, M);
      }
      w((k = k.apply(g, v || [])).next());
    });
  };
  let { margin: a = !0 } = e;
  const r = lt([0, 0]);
  nt(l, r, (g) => t(1, n = g));
  const s = lt([0, 0]);
  nt(l, s, (g) => t(2, i = g));
  let o;
  function u() {
    return f(this, void 0, void 0, function* () {
      yield Promise.all([r.set([125, 140]), s.set([-125, -140])]), yield Promise.all([r.set([-125, 140]), s.set([125, -140])]), yield Promise.all([r.set([-125, 0]), s.set([125, -0])]), yield Promise.all([r.set([125, 0]), s.set([-125, 0])]);
    });
  }
  function c() {
    return f(this, void 0, void 0, function* () {
      yield u(), o || c();
    });
  }
  function b() {
    return f(this, void 0, void 0, function* () {
      yield Promise.all([r.set([125, 0]), s.set([-125, 0])]), c();
    });
  }
  return kn(() => (b(), () => o = !0)), l.$$set = (g) => {
    "margin" in g && t(0, a = g.margin);
  }, [a, n, i, r, s];
}
class qn extends mn {
  constructor(e) {
    super(), hn(this, e, yn, vn, pn, { margin: 0 });
  }
}
const {
  SvelteComponent: Cn,
  append: se,
  attr: R,
  binding_callbacks: st,
  check_outros: zt,
  create_component: Mt,
  create_slot: Fn,
  destroy_component: Vt,
  destroy_each: Nt,
  detach: q,
  element: W,
  empty: ge,
  ensure_array_like: Ie,
  get_all_dirty_from_scope: Ln,
  get_slot_changes: Sn,
  group_outros: It,
  init: zn,
  insert: C,
  mount_component: Zt,
  noop: Oe,
  safe_not_equal: Mn,
  set_data: O,
  set_style: ne,
  space: H,
  text: Z,
  toggle_class: T,
  transition_in: oe,
  transition_out: ae,
  update_slot_base: Vn
} = window.__gradio__svelte__internal, { tick: Nn } = window.__gradio__svelte__internal, { onDestroy: In } = window.__gradio__svelte__internal, { createEventDispatcher: Zn } = window.__gradio__svelte__internal, jn = (l) => ({}), ot = (l) => ({});
function at(l, e, t) {
  const n = l.slice();
  return n[41] = e[t], n[43] = t, n;
}
function rt(l, e, t) {
  const n = l.slice();
  return n[41] = e[t], n;
}
function Pn(l) {
  let e, t, n, i, f = (
    /*i18n*/
    l[1]("common.error") + ""
  ), a, r, s;
  t = new tn({
    props: {
      Icon: rn,
      label: (
        /*i18n*/
        l[1]("common.clear")
      ),
      disabled: !1
    }
  }), t.$on(
    "click",
    /*click_handler*/
    l[32]
  );
  const o = (
    /*#slots*/
    l[30].error
  ), u = Fn(
    o,
    l,
    /*$$scope*/
    l[29],
    ot
  );
  return {
    c() {
      e = W("div"), Mt(t.$$.fragment), n = H(), i = W("span"), a = Z(f), r = H(), u && u.c(), R(e, "class", "clear-status svelte-1yk38uw"), R(i, "class", "error svelte-1yk38uw");
    },
    m(c, b) {
      C(c, e, b), Zt(t, e, null), C(c, n, b), C(c, i, b), se(i, a), C(c, r, b), u && u.m(c, b), s = !0;
    },
    p(c, b) {
      const g = {};
      b[0] & /*i18n*/
      2 && (g.label = /*i18n*/
      c[1]("common.clear")), t.$set(g), (!s || b[0] & /*i18n*/
      2) && f !== (f = /*i18n*/
      c[1]("common.error") + "") && O(a, f), u && u.p && (!s || b[0] & /*$$scope*/
      536870912) && Vn(
        u,
        o,
        c,
        /*$$scope*/
        c[29],
        s ? Sn(
          o,
          /*$$scope*/
          c[29],
          b,
          jn
        ) : Ln(
          /*$$scope*/
          c[29]
        ),
        ot
      );
    },
    i(c) {
      s || (oe(t.$$.fragment, c), oe(u, c), s = !0);
    },
    o(c) {
      ae(t.$$.fragment, c), ae(u, c), s = !1;
    },
    d(c) {
      c && (q(e), q(n), q(i), q(r)), Vt(t), u && u.d(c);
    }
  };
}
function Bn(l) {
  let e, t, n, i, f, a, r, s, o, u = (
    /*variant*/
    l[8] === "default" && /*show_eta_bar*/
    l[18] && /*show_progress*/
    l[6] === "full" && ut(l)
  );
  function c(d, L) {
    if (
      /*progress*/
      d[7]
    )
      return En;
    if (
      /*queue_position*/
      d[2] !== null && /*queue_size*/
      d[3] !== void 0 && /*queue_position*/
      d[2] >= 0
    )
      return Dn;
    if (
      /*queue_position*/
      d[2] === 0
    )
      return An;
  }
  let b = c(l), g = b && b(l), v = (
    /*timer*/
    l[5] && dt(l)
  );
  const V = [Xn, Jn], k = [];
  function N(d, L) {
    return (
      /*last_progress_level*/
      d[15] != null ? 0 : (
        /*show_progress*/
        d[6] === "full" ? 1 : -1
      )
    );
  }
  ~(f = N(l)) && (a = k[f] = V[f](l));
  let m = !/*timer*/
  l[5] && kt(l);
  return {
    c() {
      u && u.c(), e = H(), t = W("div"), g && g.c(), n = H(), v && v.c(), i = H(), a && a.c(), r = H(), m && m.c(), s = ge(), R(t, "class", "progress-text svelte-1yk38uw"), T(
        t,
        "meta-text-center",
        /*variant*/
        l[8] === "center"
      ), T(
        t,
        "meta-text",
        /*variant*/
        l[8] === "default"
      );
    },
    m(d, L) {
      u && u.m(d, L), C(d, e, L), C(d, t, L), g && g.m(t, null), se(t, n), v && v.m(t, null), C(d, i, L), ~f && k[f].m(d, L), C(d, r, L), m && m.m(d, L), C(d, s, L), o = !0;
    },
    p(d, L) {
      /*variant*/
      d[8] === "default" && /*show_eta_bar*/
      d[18] && /*show_progress*/
      d[6] === "full" ? u ? u.p(d, L) : (u = ut(d), u.c(), u.m(e.parentNode, e)) : u && (u.d(1), u = null), b === (b = c(d)) && g ? g.p(d, L) : (g && g.d(1), g = b && b(d), g && (g.c(), g.m(t, n))), /*timer*/
      d[5] ? v ? v.p(d, L) : (v = dt(d), v.c(), v.m(t, null)) : v && (v.d(1), v = null), (!o || L[0] & /*variant*/
      256) && T(
        t,
        "meta-text-center",
        /*variant*/
        d[8] === "center"
      ), (!o || L[0] & /*variant*/
      256) && T(
        t,
        "meta-text",
        /*variant*/
        d[8] === "default"
      );
      let M = f;
      f = N(d), f === M ? ~f && k[f].p(d, L) : (a && (It(), ae(k[M], 1, 1, () => {
        k[M] = null;
      }), zt()), ~f ? (a = k[f], a ? a.p(d, L) : (a = k[f] = V[f](d), a.c()), oe(a, 1), a.m(r.parentNode, r)) : a = null), /*timer*/
      d[5] ? m && (m.d(1), m = null) : m ? m.p(d, L) : (m = kt(d), m.c(), m.m(s.parentNode, s));
    },
    i(d) {
      o || (oe(a), o = !0);
    },
    o(d) {
      ae(a), o = !1;
    },
    d(d) {
      d && (q(e), q(t), q(i), q(r), q(s)), u && u.d(d), g && g.d(), v && v.d(), ~f && k[f].d(d), m && m.d(d);
    }
  };
}
function ut(l) {
  let e, t = `translateX(${/*eta_level*/
  (l[17] || 0) * 100 - 100}%)`;
  return {
    c() {
      e = W("div"), R(e, "class", "eta-bar svelte-1yk38uw"), ne(e, "transform", t);
    },
    m(n, i) {
      C(n, e, i);
    },
    p(n, i) {
      i[0] & /*eta_level*/
      131072 && t !== (t = `translateX(${/*eta_level*/
      (n[17] || 0) * 100 - 100}%)`) && ne(e, "transform", t);
    },
    d(n) {
      n && q(e);
    }
  };
}
function An(l) {
  let e;
  return {
    c() {
      e = Z("processing |");
    },
    m(t, n) {
      C(t, e, n);
    },
    p: Oe,
    d(t) {
      t && q(e);
    }
  };
}
function Dn(l) {
  let e, t = (
    /*queue_position*/
    l[2] + 1 + ""
  ), n, i, f, a;
  return {
    c() {
      e = Z("queue: "), n = Z(t), i = Z("/"), f = Z(
        /*queue_size*/
        l[3]
      ), a = Z(" |");
    },
    m(r, s) {
      C(r, e, s), C(r, n, s), C(r, i, s), C(r, f, s), C(r, a, s);
    },
    p(r, s) {
      s[0] & /*queue_position*/
      4 && t !== (t = /*queue_position*/
      r[2] + 1 + "") && O(n, t), s[0] & /*queue_size*/
      8 && O(
        f,
        /*queue_size*/
        r[3]
      );
    },
    d(r) {
      r && (q(e), q(n), q(i), q(f), q(a));
    }
  };
}
function En(l) {
  let e, t = Ie(
    /*progress*/
    l[7]
  ), n = [];
  for (let i = 0; i < t.length; i += 1)
    n[i] = ct(rt(l, t, i));
  return {
    c() {
      for (let i = 0; i < n.length; i += 1)
        n[i].c();
      e = ge();
    },
    m(i, f) {
      for (let a = 0; a < n.length; a += 1)
        n[a] && n[a].m(i, f);
      C(i, e, f);
    },
    p(i, f) {
      if (f[0] & /*progress*/
      128) {
        t = Ie(
          /*progress*/
          i[7]
        );
        let a;
        for (a = 0; a < t.length; a += 1) {
          const r = rt(i, t, a);
          n[a] ? n[a].p(r, f) : (n[a] = ct(r), n[a].c(), n[a].m(e.parentNode, e));
        }
        for (; a < n.length; a += 1)
          n[a].d(1);
        n.length = t.length;
      }
    },
    d(i) {
      i && q(e), Nt(n, i);
    }
  };
}
function _t(l) {
  let e, t = (
    /*p*/
    l[41].unit + ""
  ), n, i, f = " ", a;
  function r(u, c) {
    return (
      /*p*/
      u[41].length != null ? On : Tn
    );
  }
  let s = r(l), o = s(l);
  return {
    c() {
      o.c(), e = H(), n = Z(t), i = Z(" | "), a = Z(f);
    },
    m(u, c) {
      o.m(u, c), C(u, e, c), C(u, n, c), C(u, i, c), C(u, a, c);
    },
    p(u, c) {
      s === (s = r(u)) && o ? o.p(u, c) : (o.d(1), o = s(u), o && (o.c(), o.m(e.parentNode, e))), c[0] & /*progress*/
      128 && t !== (t = /*p*/
      u[41].unit + "") && O(n, t);
    },
    d(u) {
      u && (q(e), q(n), q(i), q(a)), o.d(u);
    }
  };
}
function Tn(l) {
  let e = de(
    /*p*/
    l[41].index || 0
  ) + "", t;
  return {
    c() {
      t = Z(e);
    },
    m(n, i) {
      C(n, t, i);
    },
    p(n, i) {
      i[0] & /*progress*/
      128 && e !== (e = de(
        /*p*/
        n[41].index || 0
      ) + "") && O(t, e);
    },
    d(n) {
      n && q(t);
    }
  };
}
function On(l) {
  let e = de(
    /*p*/
    l[41].index || 0
  ) + "", t, n, i = de(
    /*p*/
    l[41].length
  ) + "", f;
  return {
    c() {
      t = Z(e), n = Z("/"), f = Z(i);
    },
    m(a, r) {
      C(a, t, r), C(a, n, r), C(a, f, r);
    },
    p(a, r) {
      r[0] & /*progress*/
      128 && e !== (e = de(
        /*p*/
        a[41].index || 0
      ) + "") && O(t, e), r[0] & /*progress*/
      128 && i !== (i = de(
        /*p*/
        a[41].length
      ) + "") && O(f, i);
    },
    d(a) {
      a && (q(t), q(n), q(f));
    }
  };
}
function ct(l) {
  let e, t = (
    /*p*/
    l[41].index != null && _t(l)
  );
  return {
    c() {
      t && t.c(), e = ge();
    },
    m(n, i) {
      t && t.m(n, i), C(n, e, i);
    },
    p(n, i) {
      /*p*/
      n[41].index != null ? t ? t.p(n, i) : (t = _t(n), t.c(), t.m(e.parentNode, e)) : t && (t.d(1), t = null);
    },
    d(n) {
      n && q(e), t && t.d(n);
    }
  };
}
function dt(l) {
  let e, t = (
    /*eta*/
    l[0] ? `/${/*formatted_eta*/
    l[19]}` : ""
  ), n, i;
  return {
    c() {
      e = Z(
        /*formatted_timer*/
        l[20]
      ), n = Z(t), i = Z("s");
    },
    m(f, a) {
      C(f, e, a), C(f, n, a), C(f, i, a);
    },
    p(f, a) {
      a[0] & /*formatted_timer*/
      1048576 && O(
        e,
        /*formatted_timer*/
        f[20]
      ), a[0] & /*eta, formatted_eta*/
      524289 && t !== (t = /*eta*/
      f[0] ? `/${/*formatted_eta*/
      f[19]}` : "") && O(n, t);
    },
    d(f) {
      f && (q(e), q(n), q(i));
    }
  };
}
function Jn(l) {
  let e, t;
  return e = new qn({
    props: { margin: (
      /*variant*/
      l[8] === "default"
    ) }
  }), {
    c() {
      Mt(e.$$.fragment);
    },
    m(n, i) {
      Zt(e, n, i), t = !0;
    },
    p(n, i) {
      const f = {};
      i[0] & /*variant*/
      256 && (f.margin = /*variant*/
      n[8] === "default"), e.$set(f);
    },
    i(n) {
      t || (oe(e.$$.fragment, n), t = !0);
    },
    o(n) {
      ae(e.$$.fragment, n), t = !1;
    },
    d(n) {
      Vt(e, n);
    }
  };
}
function Xn(l) {
  let e, t, n, i, f, a = `${/*last_progress_level*/
  l[15] * 100}%`, r = (
    /*progress*/
    l[7] != null && mt(l)
  );
  return {
    c() {
      e = W("div"), t = W("div"), r && r.c(), n = H(), i = W("div"), f = W("div"), R(t, "class", "progress-level-inner svelte-1yk38uw"), R(f, "class", "progress-bar svelte-1yk38uw"), ne(f, "width", a), R(i, "class", "progress-bar-wrap svelte-1yk38uw"), R(e, "class", "progress-level svelte-1yk38uw");
    },
    m(s, o) {
      C(s, e, o), se(e, t), r && r.m(t, null), se(e, n), se(e, i), se(i, f), l[31](f);
    },
    p(s, o) {
      /*progress*/
      s[7] != null ? r ? r.p(s, o) : (r = mt(s), r.c(), r.m(t, null)) : r && (r.d(1), r = null), o[0] & /*last_progress_level*/
      32768 && a !== (a = `${/*last_progress_level*/
      s[15] * 100}%`) && ne(f, "width", a);
    },
    i: Oe,
    o: Oe,
    d(s) {
      s && q(e), r && r.d(), l[31](null);
    }
  };
}
function mt(l) {
  let e, t = Ie(
    /*progress*/
    l[7]
  ), n = [];
  for (let i = 0; i < t.length; i += 1)
    n[i] = pt(at(l, t, i));
  return {
    c() {
      for (let i = 0; i < n.length; i += 1)
        n[i].c();
      e = ge();
    },
    m(i, f) {
      for (let a = 0; a < n.length; a += 1)
        n[a] && n[a].m(i, f);
      C(i, e, f);
    },
    p(i, f) {
      if (f[0] & /*progress_level, progress*/
      16512) {
        t = Ie(
          /*progress*/
          i[7]
        );
        let a;
        for (a = 0; a < t.length; a += 1) {
          const r = at(i, t, a);
          n[a] ? n[a].p(r, f) : (n[a] = pt(r), n[a].c(), n[a].m(e.parentNode, e));
        }
        for (; a < n.length; a += 1)
          n[a].d(1);
        n.length = t.length;
      }
    },
    d(i) {
      i && q(e), Nt(n, i);
    }
  };
}
function bt(l) {
  let e, t, n, i, f = (
    /*i*/
    l[43] !== 0 && Yn()
  ), a = (
    /*p*/
    l[41].desc != null && gt(l)
  ), r = (
    /*p*/
    l[41].desc != null && /*progress_level*/
    l[14] && /*progress_level*/
    l[14][
      /*i*/
      l[43]
    ] != null && ht()
  ), s = (
    /*progress_level*/
    l[14] != null && wt(l)
  );
  return {
    c() {
      f && f.c(), e = H(), a && a.c(), t = H(), r && r.c(), n = H(), s && s.c(), i = ge();
    },
    m(o, u) {
      f && f.m(o, u), C(o, e, u), a && a.m(o, u), C(o, t, u), r && r.m(o, u), C(o, n, u), s && s.m(o, u), C(o, i, u);
    },
    p(o, u) {
      /*p*/
      o[41].desc != null ? a ? a.p(o, u) : (a = gt(o), a.c(), a.m(t.parentNode, t)) : a && (a.d(1), a = null), /*p*/
      o[41].desc != null && /*progress_level*/
      o[14] && /*progress_level*/
      o[14][
        /*i*/
        o[43]
      ] != null ? r || (r = ht(), r.c(), r.m(n.parentNode, n)) : r && (r.d(1), r = null), /*progress_level*/
      o[14] != null ? s ? s.p(o, u) : (s = wt(o), s.c(), s.m(i.parentNode, i)) : s && (s.d(1), s = null);
    },
    d(o) {
      o && (q(e), q(t), q(n), q(i)), f && f.d(o), a && a.d(o), r && r.d(o), s && s.d(o);
    }
  };
}
function Yn(l) {
  let e;
  return {
    c() {
      e = Z(" /");
    },
    m(t, n) {
      C(t, e, n);
    },
    d(t) {
      t && q(e);
    }
  };
}
function gt(l) {
  let e = (
    /*p*/
    l[41].desc + ""
  ), t;
  return {
    c() {
      t = Z(e);
    },
    m(n, i) {
      C(n, t, i);
    },
    p(n, i) {
      i[0] & /*progress*/
      128 && e !== (e = /*p*/
      n[41].desc + "") && O(t, e);
    },
    d(n) {
      n && q(t);
    }
  };
}
function ht(l) {
  let e;
  return {
    c() {
      e = Z("-");
    },
    m(t, n) {
      C(t, e, n);
    },
    d(t) {
      t && q(e);
    }
  };
}
function wt(l) {
  let e = (100 * /*progress_level*/
  (l[14][
    /*i*/
    l[43]
  ] || 0)).toFixed(1) + "", t, n;
  return {
    c() {
      t = Z(e), n = Z("%");
    },
    m(i, f) {
      C(i, t, f), C(i, n, f);
    },
    p(i, f) {
      f[0] & /*progress_level*/
      16384 && e !== (e = (100 * /*progress_level*/
      (i[14][
        /*i*/
        i[43]
      ] || 0)).toFixed(1) + "") && O(t, e);
    },
    d(i) {
      i && (q(t), q(n));
    }
  };
}
function pt(l) {
  let e, t = (
    /*p*/
    (l[41].desc != null || /*progress_level*/
    l[14] && /*progress_level*/
    l[14][
      /*i*/
      l[43]
    ] != null) && bt(l)
  );
  return {
    c() {
      t && t.c(), e = ge();
    },
    m(n, i) {
      t && t.m(n, i), C(n, e, i);
    },
    p(n, i) {
      /*p*/
      n[41].desc != null || /*progress_level*/
      n[14] && /*progress_level*/
      n[14][
        /*i*/
        n[43]
      ] != null ? t ? t.p(n, i) : (t = bt(n), t.c(), t.m(e.parentNode, e)) : t && (t.d(1), t = null);
    },
    d(n) {
      n && q(e), t && t.d(n);
    }
  };
}
function kt(l) {
  let e, t;
  return {
    c() {
      e = W("p"), t = Z(
        /*loading_text*/
        l[9]
      ), R(e, "class", "loading svelte-1yk38uw");
    },
    m(n, i) {
      C(n, e, i), se(e, t);
    },
    p(n, i) {
      i[0] & /*loading_text*/
      512 && O(
        t,
        /*loading_text*/
        n[9]
      );
    },
    d(n) {
      n && q(e);
    }
  };
}
function Gn(l) {
  let e, t, n, i, f;
  const a = [Bn, Pn], r = [];
  function s(o, u) {
    return (
      /*status*/
      o[4] === "pending" ? 0 : (
        /*status*/
        o[4] === "error" ? 1 : -1
      )
    );
  }
  return ~(t = s(l)) && (n = r[t] = a[t](l)), {
    c() {
      e = W("div"), n && n.c(), R(e, "class", i = "wrap " + /*variant*/
      l[8] + " " + /*show_progress*/
      l[6] + " svelte-1yk38uw"), T(e, "hide", !/*status*/
      l[4] || /*status*/
      l[4] === "complete" || /*show_progress*/
      l[6] === "hidden"), T(
        e,
        "translucent",
        /*variant*/
        l[8] === "center" && /*status*/
        (l[4] === "pending" || /*status*/
        l[4] === "error") || /*translucent*/
        l[11] || /*show_progress*/
        l[6] === "minimal"
      ), T(
        e,
        "generating",
        /*status*/
        l[4] === "generating"
      ), T(
        e,
        "border",
        /*border*/
        l[12]
      ), ne(
        e,
        "position",
        /*absolute*/
        l[10] ? "absolute" : "static"
      ), ne(
        e,
        "padding",
        /*absolute*/
        l[10] ? "0" : "var(--size-8) 0"
      );
    },
    m(o, u) {
      C(o, e, u), ~t && r[t].m(e, null), l[33](e), f = !0;
    },
    p(o, u) {
      let c = t;
      t = s(o), t === c ? ~t && r[t].p(o, u) : (n && (It(), ae(r[c], 1, 1, () => {
        r[c] = null;
      }), zt()), ~t ? (n = r[t], n ? n.p(o, u) : (n = r[t] = a[t](o), n.c()), oe(n, 1), n.m(e, null)) : n = null), (!f || u[0] & /*variant, show_progress*/
      320 && i !== (i = "wrap " + /*variant*/
      o[8] + " " + /*show_progress*/
      o[6] + " svelte-1yk38uw")) && R(e, "class", i), (!f || u[0] & /*variant, show_progress, status, show_progress*/
      336) && T(e, "hide", !/*status*/
      o[4] || /*status*/
      o[4] === "complete" || /*show_progress*/
      o[6] === "hidden"), (!f || u[0] & /*variant, show_progress, variant, status, translucent, show_progress*/
      2384) && T(
        e,
        "translucent",
        /*variant*/
        o[8] === "center" && /*status*/
        (o[4] === "pending" || /*status*/
        o[4] === "error") || /*translucent*/
        o[11] || /*show_progress*/
        o[6] === "minimal"
      ), (!f || u[0] & /*variant, show_progress, status*/
      336) && T(
        e,
        "generating",
        /*status*/
        o[4] === "generating"
      ), (!f || u[0] & /*variant, show_progress, border*/
      4416) && T(
        e,
        "border",
        /*border*/
        o[12]
      ), u[0] & /*absolute*/
      1024 && ne(
        e,
        "position",
        /*absolute*/
        o[10] ? "absolute" : "static"
      ), u[0] & /*absolute*/
      1024 && ne(
        e,
        "padding",
        /*absolute*/
        o[10] ? "0" : "var(--size-8) 0"
      );
    },
    i(o) {
      f || (oe(n), f = !0);
    },
    o(o) {
      ae(n), f = !1;
    },
    d(o) {
      o && q(e), ~t && r[t].d(), l[33](null);
    }
  };
}
var Rn = function(l, e, t, n) {
  function i(f) {
    return f instanceof t ? f : new t(function(a) {
      a(f);
    });
  }
  return new (t || (t = Promise))(function(f, a) {
    function r(u) {
      try {
        o(n.next(u));
      } catch (c) {
        a(c);
      }
    }
    function s(u) {
      try {
        o(n.throw(u));
      } catch (c) {
        a(c);
      }
    }
    function o(u) {
      u.done ? f(u.value) : i(u.value).then(r, s);
    }
    o((n = n.apply(l, e || [])).next());
  });
};
let Se = [], Ae = !1;
function Hn(l) {
  return Rn(this, arguments, void 0, function* (e, t = !0) {
    if (!(window.__gradio_mode__ === "website" || window.__gradio_mode__ !== "app" && t !== !0)) {
      if (Se.push(e), !Ae)
        Ae = !0;
      else
        return;
      yield Nn(), requestAnimationFrame(() => {
        let n = [0, 0];
        for (let i = 0; i < Se.length; i++) {
          const a = Se[i].getBoundingClientRect();
          (i === 0 || a.top + window.scrollY <= n[0]) && (n[0] = a.top + window.scrollY, n[1] = i);
        }
        window.scrollTo({ top: n[0] - 20, behavior: "smooth" }), Ae = !1, Se = [];
      });
    }
  });
}
function Kn(l, e, t) {
  let n, { $$slots: i = {}, $$scope: f } = e;
  this && this.__awaiter;
  const a = Zn();
  let { i18n: r } = e, { eta: s = null } = e, { queue_position: o } = e, { queue_size: u } = e, { status: c } = e, { scroll_to_output: b = !1 } = e, { timer: g = !0 } = e, { show_progress: v = "full" } = e, { message: V = null } = e, { progress: k = null } = e, { variant: N = "default" } = e, { loading_text: m = "Loading..." } = e, { absolute: d = !0 } = e, { translucent: L = !1 } = e, { border: M = !1 } = e, { autoscroll: w } = e, j, S = !1, I = 0, y = 0, E = null, J = null, $ = 0, B = null, h, _ = null, ee = !0;
  const re = () => {
    t(0, s = t(27, E = t(19, ve = null))), t(25, I = performance.now()), t(26, y = 0), S = !0, He();
  };
  function He() {
    requestAnimationFrame(() => {
      t(26, y = (performance.now() - I) / 1e3), S && He();
    });
  }
  function Ke() {
    t(26, y = 0), t(0, s = t(27, E = t(19, ve = null))), S && (S = !1);
  }
  In(() => {
    S && Ke();
  });
  let ve = null;
  function jt(p) {
    st[p ? "unshift" : "push"](() => {
      _ = p, t(16, _), t(7, k), t(14, B), t(15, h);
    });
  }
  const Pt = () => {
    a("clear_status");
  };
  function Bt(p) {
    st[p ? "unshift" : "push"](() => {
      j = p, t(13, j);
    });
  }
  return l.$$set = (p) => {
    "i18n" in p && t(1, r = p.i18n), "eta" in p && t(0, s = p.eta), "queue_position" in p && t(2, o = p.queue_position), "queue_size" in p && t(3, u = p.queue_size), "status" in p && t(4, c = p.status), "scroll_to_output" in p && t(22, b = p.scroll_to_output), "timer" in p && t(5, g = p.timer), "show_progress" in p && t(6, v = p.show_progress), "message" in p && t(23, V = p.message), "progress" in p && t(7, k = p.progress), "variant" in p && t(8, N = p.variant), "loading_text" in p && t(9, m = p.loading_text), "absolute" in p && t(10, d = p.absolute), "translucent" in p && t(11, L = p.translucent), "border" in p && t(12, M = p.border), "autoscroll" in p && t(24, w = p.autoscroll), "$$scope" in p && t(29, f = p.$$scope);
  }, l.$$.update = () => {
    l.$$.dirty[0] & /*eta, old_eta, timer_start, eta_from_start*/
    436207617 && (s === null && t(0, s = E), s != null && E !== s && (t(28, J = (performance.now() - I) / 1e3 + s), t(19, ve = J.toFixed(1)), t(27, E = s))), l.$$.dirty[0] & /*eta_from_start, timer_diff*/
    335544320 && t(17, $ = J === null || J <= 0 || !y ? null : Math.min(y / J, 1)), l.$$.dirty[0] & /*progress*/
    128 && k != null && t(18, ee = !1), l.$$.dirty[0] & /*progress, progress_level, progress_bar, last_progress_level*/
    114816 && (k != null ? t(14, B = k.map((p) => {
      if (p.index != null && p.length != null)
        return p.index / p.length;
      if (p.progress != null)
        return p.progress;
    })) : t(14, B = null), B ? (t(15, h = B[B.length - 1]), _ && (h === 0 ? t(16, _.style.transition = "0", _) : t(16, _.style.transition = "150ms", _))) : t(15, h = void 0)), l.$$.dirty[0] & /*status*/
    16 && (c === "pending" ? re() : Ke()), l.$$.dirty[0] & /*el, scroll_to_output, status, autoscroll*/
    20979728 && j && b && (c === "pending" || c === "complete") && Hn(j, w), l.$$.dirty[0] & /*status, message*/
    8388624, l.$$.dirty[0] & /*timer_diff*/
    67108864 && t(20, n = y.toFixed(1));
  }, [
    s,
    r,
    o,
    u,
    c,
    g,
    v,
    k,
    N,
    m,
    d,
    L,
    M,
    j,
    B,
    h,
    _,
    $,
    ee,
    ve,
    n,
    a,
    b,
    V,
    w,
    I,
    y,
    E,
    J,
    f,
    i,
    jt,
    Pt,
    Bt
  ];
}
class Qn extends Cn {
  constructor(e) {
    super(), zn(
      this,
      e,
      Kn,
      Gn,
      Mn,
      {
        i18n: 1,
        eta: 0,
        queue_position: 2,
        queue_size: 3,
        status: 4,
        scroll_to_output: 22,
        timer: 5,
        show_progress: 6,
        message: 23,
        progress: 7,
        variant: 8,
        loading_text: 9,
        absolute: 10,
        translucent: 11,
        border: 12,
        autoscroll: 24
      },
      null,
      [-1, -1]
    );
  }
}
const {
  SvelteComponent: Un,
  append: D,
  assign: Wn,
  attr: F,
  create_component: Je,
  destroy_component: Xe,
  detach: pe,
  element: U,
  get_spread_object: xn,
  get_spread_update: $n,
  init: ei,
  insert: ke,
  listen: te,
  mount_component: Ye,
  run_all: ti,
  safe_not_equal: li,
  set_data: ni,
  set_input_value: le,
  space: fe,
  text: ii,
  to_number: me,
  transition_in: Ge,
  transition_out: Re
} = window.__gradio__svelte__internal;
function fi(l) {
  let e;
  return {
    c() {
      e = ii(
        /*label*/
        l[4]
      );
    },
    m(t, n) {
      ke(t, e, n);
    },
    p(t, n) {
      n & /*label*/
      16 && ni(
        e,
        /*label*/
        t[4]
      );
    },
    d(t) {
      t && pe(e);
    }
  };
}
function si(l) {
  let e, t, n, i, f, a, r, s, o, u, c, b, g, v, V, k, N, m, d, L, M, w, j, S, I, y, E, J;
  const $ = [
    { autoscroll: (
      /*gradio*/
      l[0].autoscroll
    ) },
    { i18n: (
      /*gradio*/
      l[0].i18n
    ) },
    /*loading_status*/
    l[14]
  ];
  let B = {};
  for (let h = 0; h < $.length; h += 1)
    B = Wn(B, $[h]);
  return e = new Qn({ props: B }), e.$on(
    "clear_status",
    /*clear_status_handler*/
    l[23]
  ), f = new El({
    props: {
      show_label: (
        /*show_label*/
        l[12]
      ),
      info: (
        /*info*/
        l[5]
      ),
      $$slots: { default: [fi] },
      $$scope: { ctx: l }
    }
  }), {
    c() {
      Je(e.$$.fragment), t = fe(), n = U("div"), i = U("div"), Je(f.$$.fragment), a = fe(), r = U("div"), s = U("input"), c = fe(), b = U("input"), V = fe(), k = U("div"), N = U("div"), m = fe(), d = U("div"), L = fe(), M = U("input"), j = fe(), S = U("input"), F(s, "aria-label", o = `max input for ${/*label*/
      l[4]}`), F(s, "data-testid", "max-input"), F(s, "type", "number"), F(
        s,
        "min",
        /*minimum*/
        l[9]
      ), F(
        s,
        "max",
        /*maximum*/
        l[10]
      ), s.disabled = u = !/*interactive*/
      l[13], F(s, "class", "svelte-1dsqogo"), F(b, "aria-label", g = `min input for ${/*label*/
      l[4]}`), F(b, "data-testid", "min-input"), F(b, "type", "number"), F(
        b,
        "min",
        /*minimum*/
        l[9]
      ), F(
        b,
        "max",
        /*maximum*/
        l[10]
      ), b.disabled = v = !/*interactive*/
      l[13], F(b, "class", "svelte-1dsqogo"), F(r, "class", "numbers svelte-1dsqogo"), F(i, "class", "head svelte-1dsqogo"), F(n, "class", "wrap svelte-1dsqogo"), F(N, "class", "range-bg svelte-1dsqogo"), F(d, "class", "range-line svelte-1dsqogo"), F(
        d,
        "style",
        /*rangeLine*/
        l[17]
      ), F(M, "type", "range"), M.disabled = w = !/*interactive*/
      l[13], F(
        M,
        "min",
        /*minimum*/
        l[9]
      ), F(
        M,
        "max",
        /*maximum*/
        l[10]
      ), F(
        M,
        "step",
        /*step*/
        l[11]
      ), F(M, "class", "svelte-1dsqogo"), F(S, "type", "range"), S.disabled = I = !/*interactive*/
      l[13], F(
        S,
        "min",
        /*minimum*/
        l[9]
      ), F(
        S,
        "max",
        /*maximum*/
        l[10]
      ), F(
        S,
        "step",
        /*step*/
        l[11]
      ), F(S, "class", "svelte-1dsqogo"), F(k, "class", "range-slider svelte-1dsqogo");
    },
    m(h, _) {
      Ye(e, h, _), ke(h, t, _), ke(h, n, _), D(n, i), Ye(f, i, null), D(i, a), D(i, r), D(r, s), le(
        s,
        /*selected_max*/
        l[16]
      ), D(r, c), D(r, b), le(
        b,
        /*selected_min*/
        l[15]
      ), ke(h, V, _), ke(h, k, _), D(k, N), D(k, m), D(k, d), D(k, L), D(k, M), le(
        M,
        /*selected_min*/
        l[15]
      ), D(k, j), D(k, S), le(
        S,
        /*selected_max*/
        l[16]
      ), y = !0, E || (J = [
        te(
          s,
          "input",
          /*input0_input_handler*/
          l[24]
        ),
        te(
          b,
          "input",
          /*input1_input_handler*/
          l[25]
        ),
        te(
          M,
          "change",
          /*input2_change_input_handler*/
          l[26]
        ),
        te(
          M,
          "input",
          /*input2_change_input_handler*/
          l[26]
        ),
        te(
          M,
          "input",
          /*handle_min_change*/
          l[18]
        ),
        te(
          S,
          "change",
          /*input3_change_input_handler*/
          l[27]
        ),
        te(
          S,
          "input",
          /*input3_change_input_handler*/
          l[27]
        ),
        te(
          S,
          "input",
          /*handle_max_change*/
          l[19]
        )
      ], E = !0);
    },
    p(h, _) {
      const ee = _ & /*gradio, loading_status*/
      16385 ? $n($, [
        _ & /*gradio*/
        1 && { autoscroll: (
          /*gradio*/
          h[0].autoscroll
        ) },
        _ & /*gradio*/
        1 && { i18n: (
          /*gradio*/
          h[0].i18n
        ) },
        _ & /*loading_status*/
        16384 && xn(
          /*loading_status*/
          h[14]
        )
      ]) : {};
      e.$set(ee);
      const re = {};
      _ & /*show_label*/
      4096 && (re.show_label = /*show_label*/
      h[12]), _ & /*info*/
      32 && (re.info = /*info*/
      h[5]), _ & /*$$scope, label*/
      536870928 && (re.$$scope = { dirty: _, ctx: h }), f.$set(re), (!y || _ & /*label*/
      16 && o !== (o = `max input for ${/*label*/
      h[4]}`)) && F(s, "aria-label", o), (!y || _ & /*minimum*/
      512) && F(
        s,
        "min",
        /*minimum*/
        h[9]
      ), (!y || _ & /*maximum*/
      1024) && F(
        s,
        "max",
        /*maximum*/
        h[10]
      ), (!y || _ & /*interactive*/
      8192 && u !== (u = !/*interactive*/
      h[13])) && (s.disabled = u), _ & /*selected_max*/
      65536 && me(s.value) !== /*selected_max*/
      h[16] && le(
        s,
        /*selected_max*/
        h[16]
      ), (!y || _ & /*label*/
      16 && g !== (g = `min input for ${/*label*/
      h[4]}`)) && F(b, "aria-label", g), (!y || _ & /*minimum*/
      512) && F(
        b,
        "min",
        /*minimum*/
        h[9]
      ), (!y || _ & /*maximum*/
      1024) && F(
        b,
        "max",
        /*maximum*/
        h[10]
      ), (!y || _ & /*interactive*/
      8192 && v !== (v = !/*interactive*/
      h[13])) && (b.disabled = v), _ & /*selected_min*/
      32768 && me(b.value) !== /*selected_min*/
      h[15] && le(
        b,
        /*selected_min*/
        h[15]
      ), (!y || _ & /*rangeLine*/
      131072) && F(
        d,
        "style",
        /*rangeLine*/
        h[17]
      ), (!y || _ & /*interactive*/
      8192 && w !== (w = !/*interactive*/
      h[13])) && (M.disabled = w), (!y || _ & /*minimum*/
      512) && F(
        M,
        "min",
        /*minimum*/
        h[9]
      ), (!y || _ & /*maximum*/
      1024) && F(
        M,
        "max",
        /*maximum*/
        h[10]
      ), (!y || _ & /*step*/
      2048) && F(
        M,
        "step",
        /*step*/
        h[11]
      ), _ & /*selected_min*/
      32768 && le(
        M,
        /*selected_min*/
        h[15]
      ), (!y || _ & /*interactive*/
      8192 && I !== (I = !/*interactive*/
      h[13])) && (S.disabled = I), (!y || _ & /*minimum*/
      512) && F(
        S,
        "min",
        /*minimum*/
        h[9]
      ), (!y || _ & /*maximum*/
      1024) && F(
        S,
        "max",
        /*maximum*/
        h[10]
      ), (!y || _ & /*step*/
      2048) && F(
        S,
        "step",
        /*step*/
        h[11]
      ), _ & /*selected_max*/
      65536 && le(
        S,
        /*selected_max*/
        h[16]
      );
    },
    i(h) {
      y || (Ge(e.$$.fragment, h), Ge(f.$$.fragment, h), y = !0);
    },
    o(h) {
      Re(e.$$.fragment, h), Re(f.$$.fragment, h), y = !1;
    },
    d(h) {
      h && (pe(t), pe(n), pe(V), pe(k)), Xe(e, h), Xe(f), E = !1, ti(J);
    }
  };
}
function oi(l) {
  let e, t;
  return e = new ll({
    props: {
      visible: (
        /*visible*/
        l[3]
      ),
      elem_id: (
        /*elem_id*/
        l[1]
      ),
      elem_classes: (
        /*elem_classes*/
        l[2]
      ),
      container: (
        /*container*/
        l[6]
      ),
      scale: (
        /*scale*/
        l[7]
      ),
      min_width: (
        /*min_width*/
        l[8]
      ),
      $$slots: { default: [si] },
      $$scope: { ctx: l }
    }
  }), {
    c() {
      Je(e.$$.fragment);
    },
    m(n, i) {
      Ye(e, n, i), t = !0;
    },
    p(n, [i]) {
      const f = {};
      i & /*visible*/
      8 && (f.visible = /*visible*/
      n[3]), i & /*elem_id*/
      2 && (f.elem_id = /*elem_id*/
      n[1]), i & /*elem_classes*/
      4 && (f.elem_classes = /*elem_classes*/
      n[2]), i & /*container*/
      64 && (f.container = /*container*/
      n[6]), i & /*scale*/
      128 && (f.scale = /*scale*/
      n[7]), i & /*min_width*/
      256 && (f.min_width = /*min_width*/
      n[8]), i & /*$$scope, interactive, minimum, maximum, step, selected_max, selected_min, rangeLine, label, show_label, info, gradio, loading_status*/
      537132593 && (f.$$scope = { dirty: i, ctx: n }), e.$set(f);
    },
    i(n) {
      t || (Ge(e.$$.fragment, n), t = !0);
    },
    o(n) {
      Re(e.$$.fragment, n), t = !1;
    },
    d(n) {
      Xe(e, n);
    }
  };
}
function ai(l, e, t) {
  let n, { gradio: i } = e, { elem_id: f = "" } = e, { elem_classes: a = [] } = e, { visible: r = !0 } = e, { value: s } = e, { label: o = i.i18n("slider.slider") } = e, { info: u = void 0 } = e, { container: c = !0 } = e, { scale: b = null } = e, { min_width: g = void 0 } = e, { minimum: v = 0 } = e, { maximum: V = 100 } = e, { step: k } = e, { show_label: N } = e, { interactive: m } = e, { loading_status: d } = e, { value_is_output: L = !1 } = e;
  function M(_, ee) {
    t(20, s = [_, ee]), i.dispatch("change", [_, ee]), L || i.dispatch("input", [_, ee]);
  }
  function w(_) {
    t(15, I = parseInt(_.target.value)), I > y && t(16, y = I);
  }
  function j(_) {
    t(16, y = parseInt(_.target.value)), y < I && t(15, I = y);
  }
  let S = s, [I, y] = s;
  const E = () => i.dispatch("clear_status", d);
  function J() {
    y = me(this.value), t(16, y), t(22, S), t(20, s);
  }
  function $() {
    I = me(this.value), t(15, I), t(22, S), t(20, s);
  }
  function B() {
    I = me(this.value), t(15, I), t(22, S), t(20, s);
  }
  function h() {
    y = me(this.value), t(16, y), t(22, S), t(20, s);
  }
  return l.$$set = (_) => {
    "gradio" in _ && t(0, i = _.gradio), "elem_id" in _ && t(1, f = _.elem_id), "elem_classes" in _ && t(2, a = _.elem_classes), "visible" in _ && t(3, r = _.visible), "value" in _ && t(20, s = _.value), "label" in _ && t(4, o = _.label), "info" in _ && t(5, u = _.info), "container" in _ && t(6, c = _.container), "scale" in _ && t(7, b = _.scale), "min_width" in _ && t(8, g = _.min_width), "minimum" in _ && t(9, v = _.minimum), "maximum" in _ && t(10, V = _.maximum), "step" in _ && t(11, k = _.step), "show_label" in _ && t(12, N = _.show_label), "interactive" in _ && t(13, m = _.interactive), "loading_status" in _ && t(14, d = _.loading_status), "value_is_output" in _ && t(21, L = _.value_is_output);
  }, l.$$.update = () => {
    l.$$.dirty & /*old_value, value*/
    5242880 && JSON.stringify(S) !== JSON.stringify(s) && (t(15, [I, y] = s, I, (t(16, y), t(22, S), t(20, s))), t(22, S = s)), l.$$.dirty & /*selected_min, selected_max*/
    98304 && M(I, y), l.$$.dirty & /*selected_min, minimum, maximum, selected_max*/
    99840 && t(17, n = `
      left: ${(I - v) / (V - v) * 100}%;
      width: ${(y - I) / (V - v) * 100}%;
    `);
  }, [
    i,
    f,
    a,
    r,
    o,
    u,
    c,
    b,
    g,
    v,
    V,
    k,
    N,
    m,
    d,
    I,
    y,
    n,
    w,
    j,
    s,
    L,
    S,
    E,
    J,
    $,
    B,
    h
  ];
}
class ri extends Un {
  constructor(e) {
    super(), ei(this, e, ai, oi, li, {
      gradio: 0,
      elem_id: 1,
      elem_classes: 2,
      visible: 3,
      value: 20,
      label: 4,
      info: 5,
      container: 6,
      scale: 7,
      min_width: 8,
      minimum: 9,
      maximum: 10,
      step: 11,
      show_label: 12,
      interactive: 13,
      loading_status: 14,
      value_is_output: 21
    });
  }
}
export {
  ri as default
};
