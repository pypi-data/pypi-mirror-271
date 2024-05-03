use std::any::Any;
use std::borrow::Borrow;
use std::collections::HashMap;
use std::fmt::Display;
use std::hash::Hash;

#[derive(Default)]
pub struct AnyMap<K>(HashMap<K, Box<dyn Any + Sync + Send>>);

impl<K: Hash + Eq> AnyMap<K> {
    pub fn contains_key<Q: ?Sized + Hash + Eq>(&self, key: &Q) -> bool
        where
            K: Borrow<Q>, {
        return self.0.contains_key(&key);
    }

    pub fn insert<T: Any + Sync + Send>(&mut self, key: K, value: T) {
        self.0.insert(key, Box::new(value));
    }

    pub fn get<T: Any + Sync + Send, Q: ?Sized + Hash + Eq>(&self, key: &Q) -> &T
        where K: Borrow<Q>,
    {
        self.0.get(key).expect("Tag not found").downcast_ref::<T>().expect("Type cast error")
    }

    pub fn get_untyped<Q: ?Sized + Hash + Eq>(&self, key: &Q) -> Option<&Box<dyn Any + Sync + Send>>
        where K: Borrow<Q>,
    {
        self.0.get(key)
    }

    pub fn get_display<Q: ?Sized + Hash + Eq>(&self, key: &Q) -> &Box<dyn Display + Sync + Send>
        where
            K: Borrow<Q>,
    {
        self.0.get(key).unwrap().downcast_ref().unwrap()
    }
}