// src/components/FilterSection.tsx
interface FilterSectionProps {
    onlyOnline: boolean;
    onToggle: () => void;
}

const FilterSection = ({ onlyOnline, onToggle }: FilterSectionProps) => {
    return (
        <div className="flex items-center justify-center space-x-4 pb-8">
            <span className={`text-sm font-medium ${!onlyOnline ? 'text-white' : 'text-slate-500'}`}>All Members</span>
            <button
                onClick={onToggle}
                className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 focus:ring-offset-slate-950 ${onlyOnline ? 'bg-indigo-600' : 'bg-slate-700'}`}
            >
                <span
                    className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${onlyOnline ? 'translate-x-6' : 'translate-x-1'}`}
                />
            </button>
            <span className={`text-sm font-medium ${onlyOnline ? 'text-white' : 'text-slate-500'}`}>Online Only</span>
        </div>
    );
};

export default FilterSection;
