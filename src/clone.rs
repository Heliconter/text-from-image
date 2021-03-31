/// `clone!` is executed before compilation. Example:
/// ```rust
/// clone!(a, b as c)
/// // equals to:
/// let a = a.clone();
/// let c = b.clone();
/// ```
#[macro_export]
macro_rules! clone {
    ($var:ident) => {
        let $var = $var.clone();
    };
    ($var:ident as $alias:ident) => {
        let $alias = $var.clone();
    };
    ($($e:ident $(as $a:ident)?),*) => {
        $(
            clone!($e $(as $a)?);
        )*
    };
}
