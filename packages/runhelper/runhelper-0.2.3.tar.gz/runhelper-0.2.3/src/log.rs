use std::sync::Mutex;
use std::time::{Duration, Instant};
use log::info;

use lazy_static::lazy_static;

use crate::hashany::AnyMap;

static TAGS_LOCK_MSG: &str = "Could not lock TAGS store";

lazy_static! {
    static ref TAGS: Mutex<AnyMap<&'static str>> = {
        Mutex::new(AnyMap::default())
    };
}

lazy_static! {
    static ref TAGS_HELPER: Mutex<AnyMap<&'static str>> = {
        Mutex::new(AnyMap::default())
    };
}

#[macro_export]
macro_rules! log_any {
    ($tag:expr, $value:expr) => {
        info!("runhelper.{}={}", $tag, $value)
    };
}

macro_rules! log_tag {
    ($tag:expr) => {
        info!("runhelper.{}={}", $tag, TAGS.lock().expect(TAGS_LOCK_MSG).get_display($tag))
    };
}

pub fn set_tag<T: Sized + Send + Sync + 'static>(tag: &'static str, value: T) {
    TAGS.lock().expect(TAGS_LOCK_MSG).insert(tag, Box::new(value));
}

pub fn timer_start(tag: &'static str) {
    if !TAGS.lock().expect(TAGS_LOCK_MSG).contains_key(tag) {
        set_tag(tag, &0f64);
    }
    TAGS_HELPER.lock().expect(TAGS_LOCK_MSG).insert(tag, Instant::now());
}

pub fn timer_stop(tag: &'static str) {
    let now = Instant::now();
    let previous_instant: Instant = *TAGS_HELPER
        .lock()
        .expect(TAGS_LOCK_MSG)
        .get::<Instant, _>(tag);

    let duration = now.duration_since(previous_instant);
    let mut guard = TAGS.lock().expect(TAGS_LOCK_MSG);
    let old_duration = *guard.get::<f64, _>(tag);
    guard.insert(tag, Box::new(old_duration + duration.as_secs_f64()));
}

mod tests {
    use std::thread::sleep;

    use log::LevelFilter;
    use simplelog::{ColorChoice, Config, TerminalMode, TermLogger};

    use super::*;

    #[test]
    fn it_works() {
        TermLogger::init(LevelFilter::Info, Config::default(), TerminalMode::Stderr, ColorChoice::Auto).expect("TODO: panic message");
        log_any!("time", 34.2);
        timer_start("time2");
        sleep(Duration::new(0, 34));
        timer_stop("time2");
        log_tag!("time2");
    }
}