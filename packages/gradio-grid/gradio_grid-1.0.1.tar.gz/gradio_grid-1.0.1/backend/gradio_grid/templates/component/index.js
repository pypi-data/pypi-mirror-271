const {
  SvelteComponent: v,
  attr: u,
  create_slot: h,
  detach: b,
  element: w,
  get_all_dirty_from_scope: C,
  get_slot_changes: j,
  init: M,
  insert: T,
  null_to_empty: r,
  safe_not_equal: q,
  toggle_class: f,
  transition_in: E,
  transition_out: H,
  update_slot_base: I
} = window.__gradio__svelte__internal, { onMount: L } = window.__gradio__svelte__internal, S = (s) => ({}), g = (s) => ({ class: "test" });
function k(s) {
  let e, a, i;
  const o = (
    /*#slots*/
    s[6].default
  ), l = h(
    o,
    s,
    /*$$scope*/
    s[5],
    g
  );
  return {
    c() {
      e = w("div"), l && l.c(), u(
        e,
        "id",
        /*elem_id*/
        s[0]
      ), u(e, "class", a = r(
        /*elem_classes*/
        s[1].join(" ")
      ) + " svelte-gmnvt1"), f(
        e,
        "panel",
        /*variant*/
        s[3] === "panel"
      ), f(e, "hide", !/*visible*/
      s[2]);
    },
    m(t, _) {
      T(t, e, _), l && l.m(e, null), i = !0;
    },
    p(t, [_]) {
      l && l.p && (!i || _ & /*$$scope*/
      32) && I(
        l,
        o,
        t,
        /*$$scope*/
        t[5],
        i ? j(
          o,
          /*$$scope*/
          t[5],
          _,
          S
        ) : C(
          /*$$scope*/
          t[5]
        ),
        g
      ), (!i || _ & /*elem_id*/
      1) && u(
        e,
        "id",
        /*elem_id*/
        t[0]
      ), (!i || _ & /*elem_classes*/
      2 && a !== (a = r(
        /*elem_classes*/
        t[1].join(" ")
      ) + " svelte-gmnvt1")) && u(e, "class", a), (!i || _ & /*elem_classes, variant*/
      10) && f(
        e,
        "panel",
        /*variant*/
        t[3] === "panel"
      ), (!i || _ & /*elem_classes, visible*/
      6) && f(e, "hide", !/*visible*/
      t[2]);
    },
    i(t) {
      i || (E(l, t), i = !0);
    },
    o(t) {
      H(l, t), i = !1;
    },
    d(t) {
      t && b(e), l && l.d(t);
    }
  };
}
function y(s, e, a) {
  let { $$slots: i = {}, $$scope: o } = e, { elem_id: l } = e, { elem_classes: t = [] } = e, { visible: _ = !0 } = e, { variant: c = "default" } = e, { columns: m = 3 } = e;
  return L(() => {
    let n = "1fr ".repeat(m).trim() + "!important";
    const d = document.createElement("style");
    document.head.appendChild(d), d.innerHTML = `#${l} .form {grid-template-columns: ${n};}`;
  }), s.$$set = (n) => {
    "elem_id" in n && a(0, l = n.elem_id), "elem_classes" in n && a(1, t = n.elem_classes), "visible" in n && a(2, _ = n.visible), "variant" in n && a(3, c = n.variant), "columns" in n && a(4, m = n.columns), "$$scope" in n && a(5, o = n.$$scope);
  }, [l, t, _, c, m, o, i];
}
class z extends v {
  constructor(e) {
    super(), M(this, e, y, k, q, {
      elem_id: 0,
      elem_classes: 1,
      visible: 2,
      variant: 3,
      columns: 4
    });
  }
}
export {
  z as default
};
