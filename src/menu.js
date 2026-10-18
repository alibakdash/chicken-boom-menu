/** @typedef {{ id: string, name: string, desc: string, price: number }} MenuItem */
/** @typedef {{ id: string, title: string, icon: string, image: string, tone: 'cream' | 'red', items: MenuItem[] }} Category */

/** @type {Category[]} */
export const categories = [
  {
    id: 'fried',
    title: 'المقلي',
    icon: '🔥',
    image: '/cats/fried.jpg',
    tone: 'cream',
    items: [
      { id: 'chicken-boom', name: 'تشكن بوم', desc: 'دجاج مقلي، حبش مدخن، جبنة موزاريلا، صوص خاص', price: 550 },
      { id: 'fire-boom', name: 'فاير بوم', desc: 'دجاج مقلي، هالبينو، سلامي، تشيدر', price: 550 },
      { id: 'malibu', name: 'ماليبو', desc: 'اسكالوب، حبش مدخن، موزاريلا', price: 500 },
      { id: 'supreme', name: 'سوبريم', desc: 'قطع اسكالوب، فطر، بيبروني، موزاريلا', price: 500 },
      { id: 'crispy-boom', name: 'كريسبي بوم', desc: 'دجاج مقلي، باربكيو، حبش مدخن، موزاريلا', price: 550 },
      { id: 'crunchy', name: 'كرانشي', desc: 'دجاج مقلي، موزاريلا، تشيدر، حبش مدخن', price: 650 },
      { id: 'twister', name: 'تويستر', desc: 'دجاج مقلي، ذرة، بيبروني، تشيدر', price: 500 },
    ],
  },
  {
    id: 'grilled',
    title: 'المشوي',
    icon: '🍗',
    image: '/cats/grilled.jpg',
    tone: 'red',
    items: [
      { id: 'fax-mix', name: 'فكس مكس', desc: 'فتايل مشوية، بصل مشوي، فليفلة، بندورة، باربكيو', price: 500 },
      { id: 'fajita', name: 'فهيتا', desc: 'دجاج مشوي، بصل، فليفلة، فطر، ذرة، موزاريلا', price: 450 },
      { id: 'magnum', name: 'ماغنوم', desc: 'دجاج مشوي، فليفلة، فطر، ذرة، بيبروني، موزاريلا', price: 550 },
      { id: 'brusilia', name: 'بروسيليا', desc: 'دجاج مشوي، فليفلة، فطر، هوت دوغ، موزاريلا، كريمة', price: 500 },
      { id: 'francisco', name: 'فرانشيسكو', desc: 'دجاج مشوي، فطر، ذرة، موزاريلا', price: 450 },
      { id: 'philadelphia', name: 'فيلاديلفيا', desc: 'شرحات مشوية، بصل، فليفلة، فطر، موزاريلا', price: 600 },
      { id: 'mexican', name: 'ميكسيكان', desc: 'دجاج مشوي، بصل، فليفلة، ذرة، فطر، صوص حار، موزاريلا', price: 600 },
      { id: 'cream-strips', name: 'شرحات كريمة', desc: 'شرحات مشوية، فطر، كريمة، موزاريلا', price: 450 },
      { id: 'shish', name: 'شيش طاووق', desc: 'شيش مشوي، سلطة كولسلو، بطاطا', price: 400 },
      { id: 'chicken-sub', name: 'تشكن ساب', desc: 'شرحات مشوية، خس، ذرة، مخلل، موزاريلا', price: 450 },
    ],
  },
  {
    id: 'beef-burger',
    title: 'برغر لحمة',
    icon: '🍔',
    image: '/cats/beef-burger.jpg',
    tone: 'cream',
    items: [
      { id: 'mushroom-burger', name: 'ماشروم برغر', desc: 'لحمة، مايونيز، خس، صوص الماشروم', price: 600 },
      { id: 'cheese-burger', name: 'تشيز برغر', desc: 'لحمة، مايونيز، خس، بصل، تشيدر', price: 500 },
      { id: 'classic-burger', name: 'كلاسيك برغر', desc: 'لحمة، خس، بندورة، بصل', price: 550 },
    ],
  },
  {
    id: 'chicken-burger',
    title: 'برغر دجاج',
    icon: '🐔',
    image: '/cats/chicken-burger.jpg',
    tone: 'red',
    items: [
      {
        id: 'boom-grilled',
        name: 'برغر بوم مشوي',
        desc: 'دجاج مشوي، خس، مايونيز، صوص من اختيارك (تشيدر، باربكيو، هاني ماسترد)',
        price: 400,
      },
      {
        id: 'boom-fried',
        name: 'برغر بوم مقلي',
        desc: 'دجاج مقلي، خس، مايونيز، صوص من اختيارك (تشيدر، باربكيو، هاني ماسترد)',
        price: 400,
      },
    ],
  },
  {
    id: 'sides',
    title: 'المقبلات',
    icon: '🍟',
    image: '/cats/sides.jpg',
    tone: 'cream',
    items: [
      { id: 'fries', name: 'بطاطا', desc: '', price: 250 },
      { id: 'cheddar-fries', name: 'بطاطا تشيدر', desc: '', price: 450 },
      { id: 'jalapeno-fries', name: 'بطاطا تشيدر هالبينو', desc: '', price: 450 },
      { id: 'onion-rings', name: 'حلقات بصل مقلي', desc: '', price: 250 },
      { id: 'corn-salad', name: 'سلطة ذرة', desc: '', price: 250 },
      { id: 'caesar', name: 'سلطة سيزر', desc: '', price: 400 },
      { id: 'pasta', name: 'باستا', desc: '', price: 250 },
    ],
  },
];
