use std::fs;
fn fuel_required(&mass: &i32) -> i32 {
	return (&mass / 3).checked_sub(2).unwrap();
}


fn recursive_fuel(&mass: &i32) -> i32 {

	let mut res: i32 = fuel_required(&mass);
	let mut total: i32 = 0;
	while res > 0 {
		// println!("Iter: {}. Total: {}", res, total);
		total += res;
		res = fuel_required(&res);
	}
	total
}

fn part1() {

	println!("Part 1");
    let contents = fs::read_to_string("input.txt").expect("Unable to parse file");
    let mut total: i32 = 0;
    let mut count: usize = 0;
    
    for line in contents.lines() {
    	let val: i32 = line.trim().parse().unwrap();
    	let res: i32 = fuel_required(&val);
    	total += res;
    	count += 1;
    }

    println!("Count: {}. Total Fuel Required: {}", count, total);
    // Count: 100. Total Fuel Required: 3299598

}

fn part2() {
	println!("Part 2");
	let contents = fs::read_to_string("input.txt").expect("Unable to parse file");
    let mut total: i32 = 0;
    let mut count: usize = 0;
    
    for line in contents.lines() {
    	let val: i32 = line.trim().parse().unwrap();
    	let res: i32 = recursive_fuel(&val);
    	total += res;
    	count += 1;
    }

    println!("Count: {}. Total Fuel Required: {}", count, total);
    // Count: 100. Total Fuel Required: 4946546

}

fn main() {
	part1();
	part2();
}

#[cfg(test)]
mod tests {
	use super::*;

	#[test]
	fn fuel_tests(){
		assert_eq!(fuel_required(&12), 2);
		assert_eq!(fuel_required(&14), 2);
		assert_eq!(fuel_required(&1969), 654);
		assert_eq!(fuel_required(&100756), 33583);
		assert_eq!(fuel_required(&5), -1);
	}
	#[test]
	fn part2_tests(){
		assert_eq!(recursive_fuel(&14), 2);
		assert_eq!(recursive_fuel(&1969), 966);
		assert_eq!(recursive_fuel(&100756), 50346);
	}
}