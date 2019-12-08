use std::fs;
fn fuel_required(mass: u32) -> Option<u32> {
	return (mass / 3).checked_sub(2);
}


fn part1() {

	println!("Part 1");
    let contents = fs::read_to_string("input.txt").expect("Unable to parse file");
    let mut total: u32 = 0;
    let mut count: usize = 0;
    
    for line in contents.lines() {
    	let val: u32 = line.trim().parse().unwrap();
    	let res: u32 = fuel_required(val).unwrap();
    	total += res;
    	count += 1;
    }

    println!("Count: {}. Total Fuel Required: {}", count, total);
    // Count: 100. Total Fuel Required: 3299598

}

fn part2() {
	println!("Part 2");
	
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
		assert_eq!(fuel_required(12).unwrap(), 2);
		assert_eq!(fuel_required(14).unwrap(), 2);
		assert_eq!(fuel_required(1969).unwrap(), 654);
		assert_eq!(fuel_required(100756).unwrap(), 33583);
	}
}