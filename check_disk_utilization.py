import os
import psutil
import argparse
import json
import xml.etree.ElementTree as ET

def get_disk_usage(path):
    try:
        usage = psutil.disk_usage(path)
        return usage.percent
    except Exception as e:
        return str(e)

def get_disk_locations():
    partitions = psutil.disk_partitions()
    locations = []

    for partition in partitions:
        location = {
            'device': partition.device,
            'mountpoint': partition.mountpoint,
            'usage_percent': get_disk_usage(partition.mountpoint)
        }
        locations.append(location)

    return locations

def display_console(locations):
    print("Disk Utilization:")
    for location in locations:
        print(f"{location['device']} - {location['mountpoint']}: {location['usage_percent']}%")

    max_location = max(locations, key=lambda x: x['usage_percent'])
    print(f"\nLocation filling the disk: {max_location['device']} - {max_location['mountpoint']}")

def save_to_html(locations):
    with open("output.html", 'w') as file:
        file.write("<html><head><title>Disk Utilization</title></head><body>")
        file.write("<h2>Disk Utilization:</h2>")
        file.write("<table border='1'><tr><th>Device</th><th>Mountpoint</th><th>Usage Percent</th></tr>")
        for location in locations:
            file.write(f"<tr><td>{location['device']}</td><td>{location['mountpoint']}</td><td>{location['usage_percent']}%</td></tr>")
        file.write("</table>")
        max_location = max(locations, key=lambda x: x['usage_percent'])
        file.write(f"<p>Location filling the disk: {max_location['device']} - {max_location['mountpoint']}</p>")
        file.write("</body></html>")

def save_to_json(locations):
    with open("output.json", 'w') as file:
        json.dump(locations, file, indent=2)

def save_to_xml(locations):
    root = ET.Element("disk_utilization")
    for location in locations:
        entry = ET.SubElement(root, "location")
        device = ET.SubElement(entry, "device")
        device.text = location['device']
        mountpoint = ET.SubElement(entry, "mountpoint")
        mountpoint.text = location['mountpoint']
        usage_percent = ET.SubElement(entry, "usage_percent")
        usage_percent.text = str(location['usage_percent'])

    tree = ET.ElementTree(root)
    tree.write("output.xml")

def main():
    parser = argparse.ArgumentParser(description='Check disk utilization and display or save the results in different formats.')
    parser.add_argument('-f', '--format', choices=['console', 'html', 'json', 'xml'], default='console', help='Output format (default: console)')

    args = parser.parse_args()

    disk_locations = get_disk_locations()

    if args.format == 'console':
        display_console(disk_locations)
    elif args.format == 'html':
        save_to_html(disk_locations)
    elif args.format == 'json':
        save_to_json(disk_locations)
    elif args.format == 'xml':
        save_to_xml(disk_locations)

if __name__ == "__main__":
    main()
