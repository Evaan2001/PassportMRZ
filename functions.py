def format_date(input_date, is_expiration_date=False):
    from datetime import date

    current_year = date.today().year

    year = input_date[0:2]
    month = input_date[2:4]
    day = input_date[4:]

    reference_date = current_year % 100
    if is_expiration_date is True:
        reference_date = reference_date + 10

    if int(year) > reference_date:
        year = "19" + year
    else:
        year = "20" + year

    formatted_date = month + "/" + day + "/" + year
    return formatted_date


def update_autocorrect_dict(my_autocorrect, new_words):
    for word in new_words:
        word = word.upper()
        if word in my_autocorrect.nlp_data and my_autocorrect.nlp_data[word] > 500000:
            continue
        my_autocorrect.nlp_data[word] = 500000


def uppercase_autocorrect_dict(my_autocorrect):
    new_dict = {}
    for key, value in my_autocorrect.nlp_data.items():
        new_dict[key.upper()] = value

    my_autocorrect.nlp_data = new_dict


def preliminary_correction(name):
    name = name.strip()
    new_name = name + "  "
    for i in range(len(name)):
        if name[i].isspace() and name[i + 1].isspace():
            new_name = name[0:i]
            break
        if (
            name[i].isspace()
            and name[i + 1] == "K"
            and (name[i + 2] == "K" or name[i + 2].isspace())
        ):
            new_name = name[0:i]
            break

    return new_name.strip()


""" Helper Function"""


def k_proportion(name):
    k_count = 0
    for char in name:
        if char == "K":
            k_count = k_count + 1
    return k_count / len(name)


def advanced_correction(name):
    new_name = name.strip()
    list_of_names = new_name.split()
    output = ""

    for name_part in list_of_names:
        if k_proportion(name_part) > 0.25:
            name_part = name_part.strip("K")
        output = output + " " + name_part

    output = output.strip()
    return output


def run_mrz(image_list, path_to_image_directory):
    from passporteye import read_mrz
    from autocorrect import Speller

    my_autocorrect = Speller()
    new_names_for_autocorrect = []  # ["Evaan", "Yaser", "Ahmed"]
    update_autocorrect_dict(my_autocorrect, new_names_for_autocorrect)
    uppercase_autocorrect_dict(my_autocorrect)

    for image_name in image_list:
        full_path = path_to_image_directory + image_name
        print("\n------------------\n")
        print('For image "' + image_name + '"')
        # Get all possible data
        mrz = read_mrz(full_path)
        if mrz is None:
            print("Couldn't Process / Not A Passport")
            continue
        data = mrz.to_dict()
        # Now select relevant fields
        country = data["country"].strip("<")
        print("Country - " + country)
        passport_number = data["number"].strip("<")
        print("Passport Number - " + passport_number)
        dob = format_date(data["date_of_birth"].strip("<"), False)
        print("Date of Birth - " + dob)
        expiration = format_date(data["expiration_date"].strip("<"), True)
        print("Passport Expiration Date - " + expiration)
        sex = data["sex"].strip("<")
        print("Sex - " + sex)
        first_name = data["names"].strip("<")
        surname = data["surname"].strip("<")
        print("Original Names ->" + "\n\t" + first_name + ".\n\t" + surname + ".")
        first_name = preliminary_correction(first_name)
        surname = preliminary_correction(surname)
        print(
            "Preliminary Correction ->" + "\n\t" + first_name + ".\n\t" + surname + "."
        )
        first_name = advanced_correction(first_name)
        surname = advanced_correction(surname)
        print("Advanced Correction ->" + "\n\t" + first_name + ".\n\t" + surname + ".")


if __name__ == "__main__":
    path_to_image_directory = "sample_data/"

    image_list1 = ["usa1.jpg", "usa2.jpg", "usa2-zoomed_out.jpg", "random.jpg"]
    image_list2 = ["canada1.jpg", "canada2.jpg", "mexican1.jpg", "mexican2.jpg"]
    image_list3 = ["rotated0.jpg", "rotated90.jpg", "rotated180.jpg"]
    image_list4 = ["notpassport1.jpg", "notpassport2.jpg"]

    run_mrz(image_list4, path_to_image_directory)
